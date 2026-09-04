import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import transforms


image = Image.open("encrypted_image.tiff")

# Convert the image to a NumPy array
encrypted_image = np.array(image)

engine = transforms.ArbitraryLengthFFT()

# the key row is the "humble" one: smallest value of any column
key_index = int(np.argmin(encrypted_image[:, 0]))
key = encrypted_image[key_index].astype(np.float64)
KEY = engine.transform(key)

# circular convolution property: E(k) = X(k) . KEY(k)  ->  X(k) = E(k) / KEY(k)
decrypted_image = np.array([
    np.real(engine.inverse(engine.transform(row.astype(np.float64)) / KEY))
    for row in encrypted_image
])
decrypted_image[key_index] = key            # the key row was left unencrypted

print("Key row index:", key_index)

plt.figure(figsize=(8, 6))

# Encrypted image
plt.subplot(1, 2, 1)
plt.imshow(encrypted_image, cmap='gray')
plt.title("Encrypted Image")
plt.axis('off')

# Decrypted image
plt.subplot(1, 2, 2)
plt.imshow(decrypted_image, cmap='gray')
plt.title("Decrypted Image")
plt.axis('off')

plt.show()
