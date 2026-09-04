import cv2
import numpy as np

import transforms


def reconstruct_image_using_fft(original_path, shifted_path, output_path):
    original_img = cv2.imread(original_path)
    shifted_img = cv2.imread(shifted_path)

    orig_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY).astype(np.float64)
    shift_gray = cv2.cvtColor(shifted_img, cv2.COLOR_BGR2GRAY).astype(np.float64)

    engine = transforms.ArbitraryLengthFFT()
    reconstructed_img = np.empty_like(shifted_img)

    for r in range(orig_gray.shape[0]):
        # circular cross-correlation: peak sits at the shift that was applied
        corr = engine.inverse(
            np.conj(engine.transform(orig_gray[r])) * engine.transform(shift_gray[r])
        )
        shift = int(np.argmax(np.real(corr)))
        reconstructed_img[r] = np.roll(shifted_img[r], -shift, axis=0)

    cv2.imwrite(output_path, reconstructed_img)
    print("Max difference from original:", np.abs(reconstructed_img.astype(int) - original_img.astype(int)).max())


if __name__ == "__main__":
    reconstruct_image_using_fft("original_image.png", "shifted_image.jpg", "reconstructed_image_fft.jpg")
