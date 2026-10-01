"""
P2 -- Recover the period of a noisy periodic signal.

Autocorrelation via the Wiener-Khinchin route: r = IDFT(|X|^2). Noise is
uncorrelated with itself at nonzero lag, so it collapses into the lag-0
spike and leaves the periodic structure standing.
"""
import numpy as np

import transforms

x = np.load("data/periodic.npy")
x = x - x.mean()                             # kill DC, it swamps everything

engine = transforms.ArbitraryLengthFFT()
X = engine.transform(x)
r = np.real(engine.inverse(X * np.conj(X)))  # |X|^2 -> autocorrelation

half = r.size // 2
# r decays smoothly away from lag 0, so a plain argmax would just return 1.
# Walk past the main lobe first: the period peak is the tallest lag AFTER
# the autocorrelation has gone negative once.
first_neg = int(np.argmax(r[:half] < 0))
period = first_neg + int(np.argmax(r[first_neg:half]))

print("signal length :", x.size)
print("main lobe ends at lag:", first_neg)
print("detected period:", period)
print("r[period]/r[0] =", round(r[period] / r[0], 3))
