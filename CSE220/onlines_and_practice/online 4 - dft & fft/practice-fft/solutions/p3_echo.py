"""
P3 -- Find and remove a circular echo.

  y[n] = x[n] + a * x[(n - d) mod N]      a = 0.6, d unknown

Finding d: the CEPSTRUM. Y = X.H, so |Y|^2 = |X|^2 . |H|^2 and

    log|Y|^2 = log|X|^2 + log|H|^2

The log turns the echo's multiplicative ripple into an additive one, and
that ripple is periodic in k with period N/d -- so one more inverse
transform puts a sharp spike at lag d.

Removing it: divide the spectrum by H, since Y = X . H.
"""
import numpy as np

import transforms

ALPHA = 0.6

y = np.load("data/echoed.npy")
engine = transforms.ArbitraryLengthFFT()
N = y.size

# --- step 1: cepstrum -> the delay ---------------------------------------
Y = engine.transform(y)
cepstrum = np.real(engine.inverse(np.log(np.abs(Y) ** 2 + 1e-12)))
delay = 1 + int(np.argmax(cepstrum[1:N // 2]))

# --- step 2: build the echo filter and divide it out ----------------------
h = np.zeros(N)
h[0] = 1.0
h[delay] = ALPHA
x = np.real(engine.inverse(Y / engine.transform(h)))

clean = np.load("data/speech_clean.npy")
print("detected delay:", delay)
print("cepstrum peak height:", round(cepstrum[delay], 3))
print("max |recovered - clean|:", np.abs(x - clean).max())
