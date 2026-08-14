# fourier transform and parseval

import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, t):
        self.t = t
        # self.func = func
        self.values = self.get_values()

    def get_values(self):
        t = self.t
        self.values = np.zeros_like(t)
        for i in range(len(t)):
            if t[i] >= -3 and t[i] <= -1:
                self.values[i] = (t[i] + 3) ** 2
            elif t[i] >= -1 and t[i] <= 0:
                self.values[i] = (t[i] + 5)
            elif t[i] >= 0 and t[i] <= 1:
                self.values[i] = (-t[i] + 5)
            elif t[i] >= 1 and t[i] <= 3:
                self.values[i] = (t[i] - 3) ** 2

        return self.values

class CFTAnalyzer:
    def __init__(self, signal):
        self.signal = signal

    def transform(self, f_axis):
        # X(f) = integral x(t) * exp(-j*2*pi*f*t) dt, by trapezoid rule
        t, x = self.signal.t, self.signal.values
        return np.array([np.trapezoid(x * np.exp(-1j * 2 * np.pi * f * t), t)
                         for f in f_axis])

def plot(x, y, title = "Title", xlabel = "xlabel", ylabel = "ylabel"):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    t = np.linspace(-10, 10, 1001)
    f_t = Signal(t = t)
    plot(t, f_t.values, "Piecewise function f(t)", "t", "f(t)")

    cft_analyzer = CFTAnalyzer(f_t)
    f_axis = np.linspace(-10, 10, 1000)
    F_f = cft_analyzer.transform(f_axis)
    plot(f_axis, np.abs(F_f), "Magnitude spectrum |F(f)|", "f", "F(f)")

    # get |f(t)| ** 2 integration
    ls = np.trapezoid(np.abs(f_t.values) ** 2, t)

    # get |F(f)| ** 2 integration
    rs = np.trapezoid(np.abs(F_f) ** 2, f_axis)

    print(f"mse = {np.abs(ls - rs)}")