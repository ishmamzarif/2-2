"""
P1 -- Polynomial multiplication by FFT.

C(x) = A(x) * B(x). Linear convolution of the coefficient arrays, done
spectrally: pad to a power of two >= len(a)+len(b)-1, transform both,
multiply pointwise, invert.
"""
import numpy as np

import transforms

A = [3, 0, -2, 7, 1]          # 3 - 2x^2 + 7x^3 + x^4
B = [5, 4, -1]                # 5 + 4x - x^2

engine = transforms.FFTTransformer()
length = len(A) + len(B) - 1
N = transforms.next_power_of_two(length)

pa = np.zeros(N); pa[:len(A)] = A          # zero-pad: linear, not circular
pb = np.zeros(N); pb[:len(B)] = B

spectrum = engine.transform(pa) * engine.transform(pb)
coeffs = np.rint(np.real(engine.inverse(spectrum)))[:length]

print("transform length N =", N)
print("product coefficients:", coeffs.astype(np.int64))
print("matches np.convolve :", np.array_equal(coeffs, np.convolve(A, B)))
