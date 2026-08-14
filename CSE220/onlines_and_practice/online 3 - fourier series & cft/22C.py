import numpy as np
import matplotlib.pyplot as plt


class Signal:
    def __init__(self, t, func):
        self.t = t
        self.func = func
        self.values = func(t)

    def __add__(self, other):
        return Signal(self.t, lambda tau: self.func(tau) + other.func(tau))

    def time_scale(self, a):
        # x(a*t): compresses the time axis when a > 1
        return Signal(self.t, lambda tau: self.func(a * tau))

    def phase_shift(self, f0):
        # x(t) * exp(j*2*pi*f0*t): adds a phase ramp of 2*pi*f0*t
        return Signal(self.t, lambda tau: self.func(tau) * np.exp(1j * 2 * np.pi * f0 * tau))


class SignalGenerator:
    def __init__(self, t):
        self.t = t

    def square(self, width=2.0):
        # 1 for |t| <= width/2, 0 outside
        return Signal(self.t, lambda tau: np.where(np.abs(tau) <= width / 2, 1.0, 0.0))

    def triangle(self, width=4.0):
        # 1 at t = 0, falling linearly to 0 at |t| = width/2
        half = width / 2
        return Signal(self.t, lambda tau: np.where(np.abs(tau) <= half, 1.0 - np.abs(tau) / half, 0.0))


class CFTAnalyzer:
    """Continuous Fourier Transform by trapezoid rule (no np.fft)."""

    def __init__(self, signal):
        self.signal = signal

    def transform(self, f_axis):
        # X(f) = integral x(t) * exp(-j*2*pi*f*t) dt
        t = self.signal.t
        x = self.signal.values
        X = np.zeros(len(f_axis), dtype=complex)
        for i, f in enumerate(f_axis):
            integrand = x * np.exp(-1j * 2 * np.pi * f * t)
            X[i] = np.trapezoid(integrand, t)
        return X


def wrap(angle):
    # bring a phase difference into [-pi, pi), removing the 2*pi ambiguity
    return (angle + np.pi) % (2 * np.pi) - np.pi


if __name__ == "__main__":
    f_0 = 10.0          # phase shift 2*pi*f_0*t
    a = 10.0            # time compression factor

    # time axis: the pulses are narrow after compression, so keep it dense
    t = np.linspace(-5, 5, 20001)

    # x(t) = Square(t) + Triangle(t)
    gen = SignalGenerator(t)
    x_t = gen.square() + gen.triangle()

    # y(t) = x(a*t) * exp(j*2*pi*f_0*t), both steps through the framework
    y_t = x_t.time_scale(a).phase_shift(f_0)

    # frequency axis
    f_axis = np.linspace(-10, 10, 1001)

    X_f = CFTAnalyzer(x_t).transform(f_axis)
    Y_f = CFTAnalyzer(y_t).transform(f_axis)

    # theory: Y(f) = (1/|a|) * X((f - f_0)/a)
    # the CFT can be evaluated at any frequency, so X is computed directly
    # on the scaled-and-shifted axis instead of being interpolated
    X_scaled = CFTAnalyzer(x_t).transform((f_axis - f_0) / a)
    pred = X_scaled / abs(a)

    # only trust phase where the magnitude is actually meaningful
    mask = np.abs(pred) > 1e-3 * np.abs(pred).max()

    mse_mag = np.mean((np.abs(Y_f) - np.abs(pred)) ** 2)
    mse_phase = np.mean(wrap(np.angle(Y_f) - np.angle(pred)) ** 2)
    mse_phase_masked = np.mean(wrap(np.angle(Y_f[mask]) - np.angle(pred[mask])) ** 2)

    print(f"MSE of magnitude              = {mse_mag:.4e}")
    print(f"MSE of phase (whole axis)     = {mse_phase:.4e}")
    print(f"MSE of phase (significant f)  = {mse_phase_masked:.4e}")

    print(f"\nEffect of (ii), compression by a = {a:g}:")
    print("  the spectrum is stretched along f by a and its height is divided")
    print("  by |a| -- a narrower pulse in time needs a wider band in frequency.")
    print(f"Effect of (i), phase shift by 2*pi*f_0*t with f_0 = {f_0:g}:")
    print("  the whole (stretched) spectrum is translated so that it is centred")
    print("  at f = f_0 instead of f = 0. Its shape is untouched, so |X| is")
    print("  only moved, not deformed.")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0, 0].plot(t, x_t.values, label='x(t) = Square(t) + Triangle(t)')
    axes[0, 0].plot(t, np.real(y_t.values), '--', label='Re{y(t)}')
    axes[0, 0].set_xlim(-2.5, 2.5)
    axes[0, 0].set_xlabel('t'); axes[0, 0].set_title('Time domain')
    axes[0, 0].legend()

    axes[0, 1].plot(f_axis, np.abs(X_f), label='|X(f)|')
    axes[0, 1].set_xlabel('f'); axes[0, 1].set_title('Original spectrum, centred at 0')
    axes[0, 1].legend()

    axes[1, 0].plot(f_axis, np.abs(Y_f), label='|Y(f)|')
    axes[1, 0].plot(f_axis, np.abs(pred), '--', label='(1/|a|)*|X((f-f_0)/a)|')
    axes[1, 0].set_xlabel('f'); axes[1, 0].set_title('Magnitude verification')
    axes[1, 0].legend()

    axes[1, 1].plot(f_axis[mask], np.angle(Y_f[mask]), label='angle Y(f)')
    axes[1, 1].plot(f_axis[mask], np.angle(pred[mask]), '--', label='angle X((f-f_0)/a)')
    axes[1, 1].set_xlabel('f'); axes[1, 1].set_title('Phase verification')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.show()
