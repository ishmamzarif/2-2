"""
transforms.py  --  YOUR CODE GOES HERE.

The shared transform core used by BOTH tasks. Write it once; bigmul.py
(Task A) and image_conv.py (Task B) import it.

Nothing in this file may call numpy.fft, scipy.fft, numpy.convolve,
scipy.signal, or any other library routine that performs a Fourier
transform, a convolution or a correlation for you. NumPy is for array
arithmetic only.

A quick self-test you should run before touching either application:

    import numpy as np
    from transforms import DFTAnalyzer, FFTTransformer
    x = np.random.randn(64) + 1j * np.random.randn(64)
    d, f = DFTAnalyzer(), FFTTransformer()
    assert np.max(np.abs(d.transform(x) - f.transform(x))) < 1e-9
    assert np.max(np.abs(d.inverse(d.transform(x)) - x)) < 1e-9
"""

import numpy as np


def next_power_of_two(n):
    """
    Return the smallest power of two that is >= ``n`` (and at least 1).

    Both tasks need this to choose a transform length for the radix-2 FFT.
    """
    # TODO: implement this function
    power_of_two = 1
    while power_of_two < n:
        power_of_two <<= 1
    return power_of_two
    # raise NotImplementedError("Implement next_power_of_two")


class DFTAnalyzer:
    """
    The Discrete Fourier Transform, computed straight from its definition.

        Analysis:   X[k] = sum_{n=0}^{N-1} x[n] * exp(-2j*pi*k*n/N)
        Synthesis:  x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * exp(+2j*pi*k*n/N)

    How you write it is up to you -- a literal double loop, a precomputed
    table of twiddle factors indexed by (k*n) % N, or a NumPy expression --
    as long as it computes these sums directly and is not secretly an FFT.
    """

    name = "dft"

    def transform(self, x):
        """
        Forward DFT.

        Parameters
        ----------
        x : 1D array_like, length N (real or complex)

        Returns
        -------
        numpy.ndarray of complex128, shape (N,)
        """
        # TODO: implement this method
        x = np.asarray(x, dtype=np.complex128)
        X = np.zeros_like(x, dtype=np.complex128)
        N = np.size(x)
        n = np.arange(N)

        for k in range(N):
            X[k] = np.sum(x * np.exp(-1j * 2 * np.pi * k * n / N))

        return X
        # raise NotImplementedError("Implement DFTAnalyzer.transform")

    def inverse(self, spectrum):
        """
        Inverse DFT, including the 1/N factor.

        Parameters
        ----------
        spectrum : 1D array_like, length N (complex)

        Returns
        -------
        numpy.ndarray of complex128, shape (N,)
            Do NOT discard the imaginary part here -- the caller decides when
            it is safe to take .real.
        """
        # TODO: implement this method
        spectrum = np.asarray(spectrum, dtype=np.complex128)
        x = np.zeros_like(spectrum)
        N = np.size(x)
        k = np.arange(N)
        for n in range(N):
            x[n] = np.sum(spectrum * np.exp(1j * 2 * np.pi * k * n / N))

        return x / N
        # raise NotImplementedError("Implement DFTAnalyzer.inverse")


class FFTTransformer(DFTAnalyzer):
    """
    Radix-2 decimation-in-time (Cooley-Tukey) FFT, in O(N log N).

    It inherits from DFTAnalyzer so that both applications can treat the two
    interchangeably: they call ``engine.transform(...)`` and
    ``engine.inverse(...)`` without caring which engine they hold.

    Requirements:
      * Recursive or iterative (with bit-reversal permutation) -- your choice.
      * N must be a power of two; raise ValueError for any other length.
        The caller is responsible for zero-padding up to next_power_of_two.
      * The inverse must reuse the same butterfly machinery (conjugated
        twiddles, or conjugate-transform-conjugate), not a second copy of it.
      * Twiddle factors for a stage are computed once per stage, never once
        per butterfly.
    """

    name = "fft"

    def transform(self, x):
        """Forward FFT. Same contract as DFTAnalyzer.transform."""
        X = np.asarray(x, dtype=np.complex128).copy()
        N = np.size(X)

        if not self.check_if_power_of_two(N):
            raise ValueError("for FFT, length must be a power of two")

        X = self._bit_reverse(X)                       

        for s in range(1, N.bit_length()):           
            M = 1 << s                                 
            half = M // 2
            W = np.exp(-2j * np.pi * np.arange(half) / M)   

            blocks = X.reshape(-1, M)
            g = blocks[:, :half].copy()                #   g = x[l+k]
            h = W * blocks[:, half:]                   #   h = W * x[l+k+M/2]
            blocks[:, :half] = g + h                   #   x[l+k]       = g + h
            blocks[:, half:] = g - h                   #   x[l+k+M/2]   = g - h

        return X
        # raise NotImplementedError("Implement FFTTransformer.transform")

    def _bit_reverse(self, x):
        N = np.size(x)
        bits = N.bit_length() - 1
        idx = np.arange(N)
        rev = np.zeros(N, dtype=np.int64)
        for b in range(bits):                          # bit b -> bit (bits-1-b)
            rev |= ((idx >> b) & 1) << (bits - 1 - b)
        return x[rev]


    def inverse(self, spectrum):
        """Inverse FFT, including the 1/N factor."""
        # TODO: implement this method
        N = len(spectrum)
        conj = np.conj(spectrum)
        x = self.transform(conj)
        return (1 / N) * np.conj(x)
        # raise NotImplementedError("Implement FFTTransformer.inverse")

    def check_if_power_of_two(self, N):
        # every power of two will only have ONE set bit
        return N > 0 and N.bit_count() == 1


# ---------------------------------------------------------------------------
# BONUS (optional) -- arbitrary-length FFT.
#
# Delete this class if you are not attempting the bonus. If you do attempt it,
# run both tasks with --engine arbitrary and leave those output directories in
# your submission as the evidence.
# ---------------------------------------------------------------------------
class ArbitraryLengthFFT(FFTTransformer):
    """
    Bonus: an O(N log N) transform for ANY length N, not just powers of two.

    Bluestein's chirp-z algorithm is the usual route: rewrite the DFT as a
    convolution of two chirp sequences, and evaluate that convolution with a
    radix-2 FFT of length >= 2N-1. A mixed-radix Cooley-Tukey that factorises
    N is equally acceptable.

    With this engine, Task A no longer has to pad the digit arrays up to a
    power of two, and Task B no longer has to pad the image up to one.
    """

    name = "arbitrary"

    def __init__(self):
        self._cache = {}

    def _radix2(self, x):
        """
        The inherited power-of-two FFT, called WITHOUT dynamic dispatch.

        FFTTransformer.transform(self, x) pins the method to the parent class.
        Writing self.transform(x) here would dispatch back to the Bluestein
        transform below and recurse forever.
        """
        return FFTTransformer.transform(self, x)

    def _radix2_inverse(self, X):
        """Power-of-two inverse, by the same conjugate trick, on the parent."""
        M = np.size(X)
        return np.conj(self._radix2(np.conj(X))) / M

    def _chirp(self, N):
        """
        Build (and cache) the chirp factors for length N.

        Returns (M, w, B) where M is the radix-2 convolution length, w[j] is
        exp(-i*pi*j^2/N) and B is the spectrum of the chirp filter.
        """
        if N in self._cache:
            return self._cache[N]

        M = next_power_of_two(2 * N - 1)

        n = np.arange(N)

        angle = np.pi * ((n * n) % (2 * N)) / N
        w = np.exp(-1j * angle)


        b = np.zeros(M, dtype=np.complex128)
        b[:N] = np.conj(w)
        b[M - N + 1:] = np.conj(w)[:0:-1]

        self._cache[N] = (M, w, self._radix2(b))
        return self._cache[N]

    def transform(self, x):
        """
        Forward DFT of ANY length, by Bluestein's chirp-z algorithm.

        Using k*n = (k^2 + n^2 - (k-n)^2) / 2, the DFT sum

            X[k] = sum_n x[n] * exp(-2j*pi*k*n/N)

        factorises into  X[k] = w[k] * sum_n (x[n]*w[n]) * conj(w)[k-n],
        which is a linear convolution -- and a convolution can be evaluated at
        any length by padding up to a power of two and using the radix-2 FFT.
        """
        x = np.asarray(x, dtype=np.complex128)
        N = np.size(x)
        if N <= 1:
            return x.copy()
        if self.check_if_power_of_two(N):
            return self._radix2(x)          # no need to pay for Bluestein

        M, w, B = self._chirp(N)
        a = np.zeros(M, dtype=np.complex128)
        a[:N] = x * w                       # pre-chirp, zero-padded to M
        conv = self._radix2_inverse(self._radix2(a) * B)
        return w * conv[:N]                 # post-chirp, keep the first N

    def inverse(self, spectrum):
        """Inverse of any length, including the 1/N factor."""
        spectrum = np.asarray(spectrum, dtype=np.complex128)
        N = np.size(spectrum)
        if N == 0:
            return spectrum.copy()
        return np.conj(self.transform(np.conj(spectrum))) / N



class NTTTransformer:
    """
    Bonus: the same radix-2 butterflies as FFTTransformer, but in the integers
    modulo an NTT-friendly prime instead of the complex numbers.

    The FFT needs only ONE property of exp(-2j*pi/N): that it is a primitive
    Nth root of unity. Modulo a prime p, the element

        w = g**((p-1)/N) mod p        (g a primitive root mod p)

    has exactly that property, so the identical algorithm runs in Z_p -- where
    every operation is exact and there is no rounding step at all.

    MOD = 998244353 = 119 * 2**23 + 1 is chosen because 2**23 divides p-1, so a
    primitive Nth root exists for every power of two N up to 2**23.

    The price: a coefficient that reaches MOD wraps around and is lost, so
    Task A must use a smaller base than the floating-point engines do -- see
    NTT_BASE_DIGITS in bigmul.py.

    This engine works on int64 arrays, not complex128, so it is Task A only and
    deliberately does not subclass DFTAnalyzer.
    """

    name = "ntt"

    MOD = 998244353         # 119 * 2**23 + 1
    ROOT = 3                # a primitive root modulo MOD
    MAX_N = 1 << 23         # the largest power of two dividing MOD - 1

    def _check_length(self, N):
        if N < 1 or N & (N - 1):
            raise ValueError("NTT length must be a power of two, got %d" % N)
        if N > self.MAX_N:
            raise ValueError("NTT length %d exceeds 2**23 for this prime" % N)

    def _bit_reverse(self, x):
        """Decimation-in-time reordering, so the butterflies can run in place."""
        N = x.size
        bits = N.bit_length() - 1
        idx = np.arange(N)
        rev = np.zeros(N, dtype=np.int64)
        for b in range(bits):
            rev |= ((idx >> b) & 1) << (bits - 1 - b)
        return x[rev]

    def _butterflies(self, x, root):
        """Iterative radix-2, one vectorised stage at a time, all mod MOD."""
        p = self.MOD
        X = self._bit_reverse(np.asarray(x, dtype=np.int64) % p)
        N = X.size
        size = 2
        while size <= N:
            half = size // 2
            # One twiddle vector per stage, never per butterfly.
            step = pow(root, (p - 1) // size, p)
            w = np.ones(half, dtype=np.int64)
            for j in range(1, half):
                w[j] = w[j - 1] * step % p
            blocks = X.reshape(-1, size)
            # .copy() matters: blocks[:, :half] is a VIEW, and the first write
            # below would otherwise corrupt the values the second write reads.
            even = blocks[:, :half].copy()
            odd = blocks[:, half:] * w % p      # < p**2 < 2**60, safe in int64
            blocks[:, :half] = (even + odd) % p
            blocks[:, half:] = (even - odd) % p
            size *= 2
        return X

    def transform(self, x):
        """Forward NTT. Input and output are int64 arrays reduced mod MOD."""
        x = np.asarray(x, dtype=np.int64)
        self._check_length(x.size)
        return self._butterflies(x, self.ROOT)

    def inverse(self, spectrum):
        """Inverse NTT, including the modular equivalent of the 1/N factor."""
        spectrum = np.asarray(spectrum, dtype=np.int64)
        N = spectrum.size
        self._check_length(N)
        p = self.MOD
        # Fermat's little theorem gives modular inverses: x**(p-2) == x**-1.
        out = self._butterflies(spectrum, pow(self.ROOT, p - 2, p))
        return out * pow(N, p - 2, p) % p
