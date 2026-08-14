import numpy as np
import matplotlib.pyplot as plt
from cft_edge_detector import ContinuousImage, CFT2D, InverseCFT2D


class StripeFilter:
    """The noise here is a vertical stripe pattern: it varies along x only and
    is constant down every column. So it sits at one horizontal frequency u,
    spread over all vertical frequencies v -- a vertical band of the spectrum,
    not a ring. That is what has to be removed."""

    def find_noise_frequency(self, real, imag, u, u_min):
        # strongest horizontal frequency that is not part of the DC lobe
        # (u_min skips it: below that the "peak" is just the average brightness)
        magnitude = np.sqrt(real ** 2 + imag ** 2).mean(axis=0)
        outside_dc = np.abs(u) >= u_min
        return np.abs(u[outside_dc][np.argmax(magnitude[outside_dc])])

    def band_stop(self, real, imag, u, u_low, u_high):
        real = real.copy()
        imag = imag.copy()
        noise = (np.abs(u) >= u_low) & (np.abs(u) <= u_high)
        real[:, noise] = 0
        imag[:, noise] = 0
        return real, imag


# Load and preprocess the image
# (ContinuousImage already reads it as grayscale and normalises it to [0, 1])
img = ContinuousImage('noisy_image.png')
L = img.x[-1] - img.x[0]        # width of the image in continuous units
print(img.image.shape)

# show the image
plt.figure()
plt.title('Original Image')
plt.imshow(img.image, cmap='gray')
plt.axis('off')

cft2d = CFT2D(img)
real, imag = cft2d.compute_cft()
u = cft2d.u
du = u[1] - u[0]

# which frequencies are the noise?
magnitude = np.sqrt(real ** 2 + imag ** 2).mean(axis=0)
print("\nstrongest horizontal frequencies:")
for i in sorted(np.argsort(magnitude)[::-1][:6], key=lambda j: -magnitude[j]):
    print(f"  u = {u[i]:7.3f}  ({u[i] * L:5.2f} cycles across the image)"
          f"   mean magnitude = {magnitude[i]:.4f}")

filt = StripeFilter()
# ignore anything slower than one full cycle across the image: that is the
# letter's own body and the average brightness, not the stripes
u_noise = filt.find_noise_frequency(real, imag, u, u_min=1.0 / L)
print(f"\nnoise frequency: u = {u_noise:.3f}  "
      f"({u_noise * L:.2f} stripes across the image)")

# notch out that one column (+/- half a sample of the frequency axis) and its
# mirror at -u; everything else, including u = 0, is left alone
real_f, imag_f = filt.band_stop(real, imag, u, u_noise - du / 2, u_noise + du / 2)

icft2d = InverseCFT2D(real_f, imag_f, cft2d.u, cft2d.v, img.x, img.y)
denoised_image = icft2d.reconstruct()

plt.figure()
plt.title('Magnitude spectrum (averaged over v)')
plt.plot(u, magnitude)
plt.axvspan(u_noise - du / 2, u_noise + du / 2, color='red', alpha=0.4, label='removed')
plt.axvspan(-u_noise - du / 2, -u_noise + du / 2, color='red', alpha=0.4)
plt.xlim(-6, 6)
plt.xlabel('u (cycles per unit length)')
plt.legend()

plt.figure()
plt.title('Denoised Image')
plt.imshow(denoised_image, cmap='gray')
plt.axis('off')
plt.show()

# plt.imsave('denoised_image.png', denoised_image, cmap='gray')
