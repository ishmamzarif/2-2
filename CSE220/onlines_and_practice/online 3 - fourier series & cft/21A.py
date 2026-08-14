# whatever the fuck this is 

import numpy as np
import matplotlib.pyplot as plt


class ContinuousImage:
    """Loads the image as a grayscale 2D signal on a continuous x axis."""

    def __init__(self, image_path):
        image = plt.imread(image_path)
        if image.ndim == 3:
            image = np.mean(image[:, :, :3], axis=2)    # drop alpha, then grayscale
        if image.max() > 1.0:
            image = image / 255.0                       # png floats are already [0,1]

        self.image = image
        self.height, self.width = image.shape
        # every row lives on x in [-1, 1]
        self.x = np.linspace(-1, 1, self.width)
        self.L = self.x[-1] - self.x[0]

    def show(self, title):
        plt.figure()
        plt.title(title)
        plt.imshow(self.image, cmap='gray')
        plt.axis('off')


class RowCFT:
    """Fourier transform of the image row by row (hint 1), by trapezoid rule.

    Harmonic k means 'k full cycles across the width of a row', so the
    harmonic number is directly the stripe count you can see in the image."""

    def __init__(self, img):
        self.img = img
        self.x = img.x
        self.L = img.L
        self.k = np.arange(-img.width // 2, img.width // 2 + 1)

    def transform(self):
        # c[row, k] = (1/L) * integral row(x) * exp(-j*2*pi*k*x/L) dx
        C = np.zeros((self.img.height, len(self.k)), dtype=complex)
        for i, k in enumerate(self.k):
            e = np.exp(-1j * 2 * np.pi * k * self.x / self.L)
            C[:, i] = np.trapezoid(self.img.image * e, self.x, axis=1) / self.L
        return C

    def inverse(self, C):
        # row(x) = sum_k c_k * exp(+j*2*pi*k*x/L)
        rows = np.zeros((C.shape[0], len(self.x)))
        for j, xj in enumerate(self.x):
            rows[:, j] = np.real(C @ np.exp(1j * 2 * np.pi * self.k * xj / self.L))
        return rows

    def dominant_frequency(self, f_min=0.6, f_max=8.0, n_scan=800):
        # the CFT can be evaluated at ANY frequency, not just integer harmonics,
        # so scan a fine grid to locate the noise peak exactly.
        # f_min skips the DC lobe (its width is about 1/L).
        f_scan = np.linspace(f_min, f_max, n_scan)
        mag = np.zeros(n_scan)
        for i, f in enumerate(f_scan):
            e = np.exp(-1j * 2 * np.pi * f * self.x)
            mag[i] = np.abs(np.trapezoid(self.img.image * e, self.x, axis=1)).mean()
        return f_scan[np.argmax(mag)] * self.L      # in cycles across the row


class FrequencyFilter:
    """Removes a band of row-frequencies and keeps everything else."""

    def band_stop(self, C, k_axis, k_low, k_high):
        C = C.copy()
        noise = (np.abs(k_axis) >= k_low) & (np.abs(k_axis) <= k_high)
        C[:, noise] = 0
        return C


if __name__ == "__main__":
    img = ContinuousImage('noisy_image.png')
    img.show('Original (noisy) image')

    cft = RowCFT(img)
    C = cft.transform()

    # which frequencies are the noise? look at the row-averaged spectrum
    strength = np.abs(C).mean(axis=0)
    print("strongest row-harmonics (k = cycles across the image):")
    for i in np.argsort(strength)[::-1][:7]:
        print(f"  k = {cft.k[i]:4d}   mean |c_k| = {strength[i]:.4f}")

    f_noise = cft.dominant_frequency()
    k_low, k_high = int(np.floor(f_noise)), int(np.ceil(f_noise))
    print(f"\nstrongest non-DC frequency: {f_noise:.3f} cycles across the image")
    print(f"-> the stripes are the noise, so harmonics +/-{k_low} and +/-{k_high} are removed")
    print("   (k = 0 is kept: it carries the average brightness)")

    C_clean = FrequencyFilter().band_stop(C, cft.k, k_low, k_high)
    denoised = cft.inverse(C_clean)

    plt.figure()
    plt.title('Row-averaged spectrum')
    plt.plot(cft.k, strength)
    plt.axvspan(k_low, k_high, color='red', alpha=0.3, label='removed')
    plt.axvspan(-k_high, -k_low, color='red', alpha=0.3)
    plt.xlabel('k (cycles across a row)'); plt.ylabel('mean |c_k|')
    plt.xlim(-12, 12); plt.legend()

    plt.figure()
    plt.title('Recovered letter')
    plt.imshow(denoised, cmap='gray')
    plt.axis('off')
    plt.show()

    # plt.imsave('denoised_image.png', denoised, cmap='gray')
