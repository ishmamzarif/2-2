"""
P5 -- Locate a small patch inside a larger image (2D cross-correlation).

Zero-pad the patch to the scene's size, then correlate spectrally:
    C = IDFT2( conj(PATCH) * SCENE )
The peak lands on the shift that carries the padded patch (sitting at the
origin) onto its copy inside the scene -- i.e. the top-left corner.
Both are mean-removed first, otherwise the correlation just reports the
brightest region of the scene instead of the best-matching one.
"""
import numpy as np

import transforms
from image_conv import inverse_2d, transform_2d

scene = np.load("data/scene.npy")
patch = np.load("data/patch.npy")

engine = transforms.ArbitraryLengthFFT()
H, W = scene.shape
ph, pw = patch.shape

padded = np.zeros((H, W))
padded[:ph, :pw] = patch - patch.mean()

corr = np.real(inverse_2d(
    np.conj(transform_2d(padded, engine)) * transform_2d(scene - scene.mean(), engine),
    engine,
))
top, left = np.unravel_index(np.argmax(corr), corr.shape)

print("patch size:", patch.shape)
print("found at (row, col) =", (int(top), int(left)))
print("exact match:", np.allclose(scene[top:top + ph, left:left + pw], patch))
