import numpy as np
import matplotlib.pyplot as plt
class Signal:
    def __init__(self, t, func):
        self.t = t
        self.start = t[0]
        self.end =  t[-1]
        self.func = func
        self.values = func(t)

    def time_shift(self, t0):
        # y(t) = x(t - t0): no array is rolled, the function is re-sampled
        # keeps the time range of the continuous signal the same, just shifts it
        return Signal(self.t, lambda tau: self.func(tau - t0))


class SignalGenerator:
    def __init__(self, t):
        self.t = t

    def gaussian(self, a):
        # x(t) = exp(-a * t^2), a controls the width
        return Signal(self.t, lambda tau: np.exp(-a * tau ** 2))


class CFTAnalyzer:
    def __init__(self, signal):
        self.signal = signal

    def transform(self, f_axis):
        # X(f) = integral x(t) * exp(-j*2*pi*f*t) dt, by trapezoid rule
        t, x = self.signal.t, self.signal.values
        return np.array([np.trapezoid(x * np.exp(-1j * 2 * np.pi * f * t), t)
                         for f in f_axis])



def wrap(angle):
    # bring a phase difference into [-pi, pi)
    return (angle + np.pi) % (2 * np.pi) - np.pi


if __name__ == "__main__":
    # Part 2: time axis and x(t) = exp(-t^2)
    t = np.linspace(-5, 5, 2001)
    gen = SignalGenerator(t)
    x_t = gen.gaussian(a=1)

    # Part 3: y(t) = x(t - 1), done through the framework
    t_0 = 1.0
    y_t = x_t.time_shift(t_0)

    # Part 4: CFT of both signals
    f_axis = np.linspace(-10, 10, 1001)
    X_f = CFTAnalyzer(x_t).transform(f_axis)
    Y_f = CFTAnalyzer(y_t).transform(f_axis)

    # Part 6(a): magnitude MSE
    mse_mag = np.mean((np.abs(X_f) - np.abs(Y_f)) ** 2)

    # Part 6(b): phase MSE against the predicted phase
    pred_phase = np.angle(X_f) - 2 * np.pi * f_axis * t_0
    mse_phase_raw = np.mean((np.angle(Y_f) - pred_phase) ** 2)
    mse_phase = np.mean(wrap(np.angle(Y_f) - pred_phase) ** 2)

    # the Gaussian spectrum dies out very fast, so phase is only meaningful
    # where the magnitude is still above the numerical noise floor
    mask = np.abs(X_f) > 1e-6 * np.abs(X_f).max()
    mse_phase_masked = np.mean(wrap(np.angle(Y_f) - pred_phase)[mask] ** 2)

    print(f"MSE of magnitude            = {mse_mag:.4e}")
    print(f"MSE of phase (raw formula)  = {mse_phase_raw:.4e}")
    print(f"MSE of phase (wrapped)      = {mse_phase:.4e}")
    print(f"MSE of phase (significant f)= {mse_phase_masked:.4e}")
    print("\nComment: |X(f)| = |Y(f)| to machine precision, and once the 2*pi "
          "\nambiguity is wrapped out the measured phase of Y matches "
          "\nangle(X(f)) - 2*pi*f*t0. Both confirm the time-shift property. "
          "\nThe raw (unwrapped) value is large only because angle() folds the "
          "\nlinear phase ramp back into [-pi, pi].")

    # Part 5: plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0, 0].plot(t, x_t.values, label='x(t) = e^{-t^2}')
    axes[0, 0].plot(t, y_t.values, '--', label='y(t) = x(t-1)')
    axes[0, 0].set_xlabel('t'); axes[0, 0].set_title('Time domain')
    axes[0, 0].legend()

    axes[0, 1].plot(f_axis, np.abs(X_f), label='|X(f)|')
    axes[0, 1].plot(f_axis, np.abs(Y_f), '--', label='|Y(f)|')
    axes[0, 1].set_xlim(-3, 3)
    axes[0, 1].set_xlabel('f'); axes[0, 1].set_title('Magnitude spectra')
    axes[0, 1].legend()

    axes[1, 0].plot(f_axis[mask], np.angle(X_f[mask]), label='angle X(f)')
    axes[1, 0].plot(f_axis[mask], np.angle(Y_f[mask]), '--', label='angle Y(f)')
    axes[1, 0].set_xlabel('f'); axes[1, 0].set_title('Phase spectra')
    axes[1, 0].legend()

    axes[1, 1].plot(f_axis[mask], np.angle(Y_f[mask]), label='measured angle Y(f)')
    axes[1, 1].plot(f_axis[mask], wrap(pred_phase[mask]), '--',
                    label='predicted angle X(f) - 2*pi*f*t0')
    axes[1, 1].set_xlabel('f'); axes[1, 1].set_title('Phase verification')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.show()
