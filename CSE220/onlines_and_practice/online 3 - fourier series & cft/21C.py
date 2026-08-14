# fourier series, series reconstruction and plotting

import numpy as np 
import matplotlib.pyplot as plt

class FourierEpicycles:
    def __init__(self, t, signal, n_harmonics):
        self.t = t
        self.signal = signal
        self.N = n_harmonics
        self.T = t[-1]
        self.omega = 2 * np.pi / self.T
        self.coeffs = {}

    def calculate_cn(self, n):
        e = np.exp(-1j * n * self.omega * self.t)
        return np.trapezoid(self.signal * e, self.t) / self.T

    def calculate_all_coefficients(self):
        for n in range(-self.N, self.N + 1):
            self.coeffs[n] = self.calculate_cn(n)

    def approximate(self, t):
        t = np.asarray(t)
        result = np.zeros_like(t, dtype = complex)
        for n, c_n in self.coeffs.items():
            result = result + c_n * np.exp(1j * n * self.omega * t)
        return result

def plot(x, y, title = "Title", xlabel = "xlabel", ylabel = "ylabel"):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.grid(True)
    plt.show()

def stem_plot(x, y, title = "Title", xlabel = "xlabel", ylabel = "ylabel"):
    plt.figure()
    plt.stem(x, y)
    plt.title(title)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # exactly one period, starting at 0 (the class reads T off t[-1])
    t = np.linspace(0, 1, 1001)
    A = np.sin(14 * np.pi * t)
    B = np.sin(2 * np.pi * t)
    signal = 2 * A - B * (4 * A * B - 1)
    n_harmonics = 15

    plot(t, signal, "Given signal f(t)", "t", "f(t)")

    f = FourierEpicycles(t, signal, n_harmonics)
    f.calculate_all_coefficients()

    # c_n is purely imaginary for a pure-sine signal, so plot the magnitude
    harmonics = np.array(list(f.coeffs.keys()))
    magnitudes = np.abs(np.array(list(f.coeffs.values())))

    stem_plot(harmonics, magnitudes, "coeff magnitudes |c_n|", "n (no of harmonics)", "|c_n|")

    # harmonic n sits at n/T Hz, with amplitude 2|c_n| and phase angle(c_n) + pi/2
    print("components found by the Fourier transform:")
    detected = []
    for n in range(1, n_harmonics + 1):
        c_n = f.coeffs[n]
        if np.abs(c_n) > 0.01:
            detected.append(n / f.T) # n / T  = n * f = nth harmonic frequency
            print(f"  {n / f.T:5.1f} Hz   amplitude = {2 * np.abs(c_n):.4f}   "
                  f"phase = {np.angle(c_n) + np.pi / 2:+.4f} rad")


    # the summation the question asks for: only the frequencies just detected
    summation = np.zeros_like(t)
    for freq in detected:
        summation = summation + np.sin(2 * np.pi * freq * t)

    reconstructed = f.approximate(t).real


    plt.figure()
    plt.plot(t, signal, label="given f(t)")
    plt.plot(t, reconstructed, '--', label="Fourier series")
    plt.plot(t, summation, ':', label="sum of detected sines")
    plt.title("Original vs reconstruction")
    plt.xlabel("t")
    plt.ylabel("f(t)")
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"\nmse (fourier series) = {np.mean(np.abs(reconstructed - signal) ** 2)}")
    print(f"mse (detected sines) = {np.mean(np.abs(summation - signal) ** 2)}")
