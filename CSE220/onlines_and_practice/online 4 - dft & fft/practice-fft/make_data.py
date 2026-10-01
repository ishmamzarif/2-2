"""
Regenerates every input file in data/. Run once; the exam problems read
the .npy / .png files it writes.
"""
import numpy as np

from image_utils import load_image, save_image

rng = np.random.default_rng(220)

# ---- P2: a noisy periodic signal, period 37 -------------------------------
N = 1024
PERIOD = 37
n = np.arange(N)
clean = np.sin(2 * np.pi * n / PERIOD) + 0.5 * np.sin(4 * np.pi * n / PERIOD)
np.save("data/periodic.npy", clean + rng.normal(0, 0.8, N))

# ---- P3: a signal plus one delayed echo -----------------------------------
N = 2048
DELAY, ALPHA = 300, 0.6
t = np.arange(N)
speech = (np.sin(2 * np.pi * 5 * t / N) * np.exp(-3 * t / N)
          + 0.4 * np.sin(2 * np.pi * 23 * t / N)
          + 0.2 * rng.normal(0, 1, N))
np.save("data/speech_clean.npy", speech)
np.save("data/echoed.npy", speech + ALPHA * np.roll(speech, DELAY))

# ---- P5: an image and a patch cut out of it -------------------------------
img = load_image("data/skyline256.png", as_gray=True)
TOP, LEFT, PH, PW = 148, 61, 40, 52
np.save("data/scene.npy", img)
np.save("data/patch.npy", img[TOP:TOP + PH, LEFT:LEFT + PW].copy())

# ---- P6: the same image, with noise added ---------------------------------
np.save("data/clean_image.npy", img)
np.save("data/noisy_image.npy", np.clip(img + rng.normal(0, 0.14, img.shape), 0, 1))

print("data/ written. (P5 answer: top-left = (%d, %d))" % (TOP, LEFT))
