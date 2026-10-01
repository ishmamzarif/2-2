"""
P4 -- Big-integer exponentiation on top of the FFT multiplier.

7 ** 5000 by binary exponentiation, where every single multiply is the
spectral convolution in bigmul (no Python big-int multiplication).
"""
import bigmul

BASE, EXP = 7, 5000

result, acc, e = "1", str(BASE), EXP
while e:
    if e & 1:
        result = bigmul.multiply(result, acc, "fft")[0]     # [0] = the digits
    acc = bigmul.multiply(acc, acc, "fft")[0]
    e >>= 1

expected = str(BASE ** EXP)
print("digits in result:", len(result))
print("first 40:", result[:40])
print("last 20 :", result[-20:])
print("matches Python pow:", result == expected)
