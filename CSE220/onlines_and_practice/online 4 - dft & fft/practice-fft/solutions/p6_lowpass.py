"""
P6 -- Denoise an image with an ideal low-pass filter in the frequency domain.

Noise is spread over all frequencies; the picture's energy is concentrated
at low ones. Zeroing every coefficient outside a radius removes most of the
noise and only the finest detail.
"""
import numpy as np

import transforms
from image_conv import inverse_2d, transform_2d

CUTOFF = 42


def psnr(a, b):
    return 10 * np.log10(1.0 / np.mean((a - b) ** 2))


noisy = np.load("data/noisy_image.npy")
clean = np.load("data/clean_image.npy")
engine = transforms.ArbitraryLengthFFT()
H, W = noisy.shape

# frequency index k stands for the frequency min(k, N-k) -- wrap-around
fy = np.minimum(np.arange(H), H - np.arange(H))[:, None]
fx = np.minimum(np.arange(W), W - np.arange(W))[None, :]
mask = (fy ** 2 + fx ** 2) <= CUTOFF ** 2

filtered = np.real(inverse_2d(transform_2d(noisy, engine) * mask, engine))
filtered = np.clip(filtered, 0, 1)

print("kept %d of %d coefficients (%.1f%%)"
      % (mask.sum(), mask.size, 100 * mask.sum() / mask.size))
print("PSNR noisy    : %.2f dB" % psnr(noisy, clean))
print("PSNR filtered : %.2f dB" % psnr(filtered, clean))
