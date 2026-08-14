import numpy as np
import matplotlib.pyplot as plt


class Signal:
    def __init__(self, t, values, name):
        self.t = t
        self.values = values
        self.name = name

class SignalGenerator:
    def __init__(self, t):
        self.t = t

    def x(self):
        values = 0.5*np.cos(4*self.t) + 0.5*np.sin(6*self.t)
        return Signal(self.t, values, "x(t)")

    def y1(self):
        values = -2*np.sin(4*self.t) + 3*np.cos(6*self.t)
        return Signal(self.t, values, "y1(t)")

    def y2(self):
        values = -8*np.cos(4*self.t) - 18*np.sin(6*self.t)
        return Signal(self.t, values, "y2(t)")

    def y3(self):
        values = 32*np.sin(4*self.t) - 108*np.cos(6*self.t)
        return Signal(self.t, values, "y3(t)")


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
        # return np.array( [np.trapezoid(-1j * 2 * np.pi * f * t * x, t)
        #                     for f in f_axis] )


def wrap(angle):
    # bring a phase difference into [-pi, pi), removing the 2*pi ambiguity
    return (angle + np.pi) % (2 * np.pi) - np.pi


if __name__ == "__main__":
    # fundamental frequency (parentheses matter!)
    omega_0 = np.gcd(4, 6)
    f_0 = omega_0 / (2 * np.pi)
    T_0 = 1 / f_0

    # time axis: fine resolution, window = exact integer number of periods
    fs = 200
    T = 20 * T_0
    t = np.linspace(-T/2, T/2, int(fs * T) + 1)

    gen = SignalGenerator(t)
    x = gen.x()
    derivatives = [gen.y1(), gen.y2(), gen.y3()]

    # frequency axis, wide enough to hold both peaks (at 2*f_0 and 3*f_0)
    f_max = 5 * f_0
    f_axis = np.linspace(-f_max, f_max, 1000)

    X_f = CFTAnalyzer(x).transform(f_axis)
    jw = 1j * 2 * np.pi * f_axis

    # only trust phase where the magnitude is actually meaningful
    mask = np.abs(X_f) > 0.1 * np.abs(X_f).max()

    fig, axes = plt.subplots(3, 2, figsize=(11, 9))
    for n in (1, 2, 3):
        Y_f = CFTAnalyzer(derivatives[n-1]).transform(f_axis)
        pred = (jw ** n) * X_f          # theory: F{d^n x/dt^n} = (j2*pi*f)^n X(f)

        mag_mse = np.mean((np.abs(Y_f) - np.abs(pred)) ** 2)
        rel_mse = mag_mse / np.mean(np.abs(Y_f) ** 2)       # scale-free version
        phase_mse = np.mean(wrap(np.angle(Y_f[mask]) - np.angle(pred[mask])) ** 2)
        print(f"Derivative {n}: magnitude MSE = {mag_mse:.4e} "
              f"(relative {rel_mse:.4e}), phase MSE (near peaks) = {phase_mse:.4e}")

        row = n - 1
        axes[row,0].plot(f_axis, np.abs(Y_f), label=f'|Y{n}(f)|')
        axes[row,0].plot(f_axis, np.abs(pred), '--', label=f'|(j2πf)^{n} X(f)|')
        axes[row,0].legend(); axes[row,0].set_title(f'Magnitude overlap, derivative {n}')
        axes[row,1].plot(f_axis[mask], np.angle(Y_f[mask]), label=f'phase Y{n}(f)')
        axes[row,1].plot(f_axis[mask], np.angle(pred[mask]), '--', label=f'phase pred{n}')
        axes[row,1].legend(); axes[row,1].set_title(f'Phase comparison, derivative {n}')


    plt.tight_layout()
    plt.show()







