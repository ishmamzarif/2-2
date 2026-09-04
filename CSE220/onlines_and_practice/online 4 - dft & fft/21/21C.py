import numpy as np
import matplotlib.pyplot as plt

import transforms

engine = transforms.ArbitraryLengthFFT()


def circular_shift_amount(a, b):
    """Peak of the DFT cross-correlation = circular shift of b relative to a."""
    corr = engine.inverse(np.conj(engine.transform(a)) * engine.transform(b))
    return int(np.argmax(np.real(corr)))


image = plt.imread("image.png")
shifted_image = plt.imread("shifted_image.png")

# Wise choice of row/column: summing down an axis cancels that axis' shift, so
# each collapsed signal carries exactly one of the two unknowns.
dx = circular_shift_amount(image.sum(axis=0), shifted_image.sum(axis=0))
dy = circular_shift_amount(image.sum(axis=1), shifted_image.sum(axis=1))
print("Detected shift -> vertical:", dy, " horizontal:", dx)

reversed_shifted_image = np.roll(shifted_image, (-dy, -dx), axis=(0, 1))
print("Max difference from original:", np.abs(reversed_shifted_image - image).max())

plt.figure(figsize=(12, 8))

# Original Image
plt.subplot(2, 3, 1)
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.axis('off')

# Shifted Image
plt.subplot(2, 3, 2)
plt.imshow(shifted_image, cmap='gray')
plt.title(f"Shifted Image")
plt.axis('off')


# Reversed Shifted Image
plt.subplot(2, 3, 3)
plt.imshow(reversed_shifted_image, cmap='gray')
plt.title("Reversed Shifted Image")
plt.axis('off')

plt.tight_layout()
plt.show()
