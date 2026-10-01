# FFT / IFFT practice set — CSE 220

Six exam-style problems, 30–45 minutes each. Every one is solved with
`transforms.py`, `bigmul.py` or `image_conv.py` — no `numpy.fft` anywhere.

    cd practice-fft
    python3 make_data.py              # once, regenerates data/
    PYTHONPATH=. python3 solutions/p1_polymul.py

Solutions are in `solutions/`. Try each problem first; the expected output
of every solution is listed at the bottom of this file.

---

## P1 — Polynomial multiplication  ·  *easy, ~15 min*

Multiply `A(x) = 3 − 2x² + 7x³ + x⁴` by `B(x) = 5 + 4x − x²` using the FFT.

* Pad both coefficient arrays to `next_power_of_two(len(A)+len(B)−1)`.
* Transform, multiply pointwise, invert, round.
* Verify against `np.convolve`.

**Why pad?** The DFT gives you *circular* convolution. Padding to at least
`len(A)+len(B)−1` leaves room for the tail so nothing wraps — that is what
turns it into the *linear* convolution a polynomial product needs.

## P2 — Period of a noisy signal  ·  *easy, ~20 min*

`data/periodic.npy` holds 1024 samples of a periodic signal buried in heavy
noise. Recover the period.

* Autocorrelation without a loop: `r = IDFT(|X|²)` (Wiener–Khinchin).
* Noise correlates with itself only at lag 0, so it piles into `r[0]` and
  leaves the periodic peaks visible.
* **Trap:** `argmax(r[1:])` returns 1. `r` decays smoothly away from lag 0,
  so you must walk past that main lobe first — take the tallest peak *after*
  `r` first goes negative.

## P3 — Echo removal  ·  *medium, ~35 min*

`data/echoed.npy` holds `y[n] = x[n] + 0.6·x[(n−d) mod N]`. Find `d` and
recover `x`.

* Finding `d` — the **cepstrum**. Since `Y = X·H`, taking logs gives
  `log|Y|² = log|X|² + log|H|²`. The log converts the echo's multiplicative
  ripple into an additive one that is periodic in `k`, so one more inverse
  transform puts a sharp spike at lag `d`.
* Removing it — build `h = δ₀ + 0.6·δ_d`, then `X = Y / DFT(h)`.
* **Trap:** autocorrelation does *not* work here (it reports 356, not 300).
  The signal's own structure outweighs the echo peak. The cepstrum's log is
  what separates the two.

## P4 — Big-integer exponentiation  ·  *easy–medium, ~25 min*

Compute `7**5000` using `bigmul`, with **no Python big-int multiplication**.

* Binary exponentiation: square repeatedly, multiply into the accumulator
  when the exponent bit is set.
* Every multiply goes through `bigmul.multiply(a, b, "fft")`.
* Verify against Python's own `7**5000`.

## P5 — Template matching  ·  *medium, ~35 min*

`data/patch.npy` is a 40×52 crop taken from `data/scene.npy`. Find where.

* Zero-pad the patch up to the scene's shape, at the origin.
* Correlate in 2-D: `C = IDFT2( conj(PATCH) · SCENE )`, using
  `image_conv.transform_2d` / `inverse_2d`.
* `np.unravel_index(np.argmax(C), C.shape)` → the top-left corner.
* **Trap 1:** subtract the mean from both first. Raw correlation reports the
  *brightest* region, not the best-matching one.
* **Trap 2:** the conjugate goes on the **patch**. Put it on the scene and
  you get `(N−row, N−col)` — the shift measured backwards.

## P6 — Frequency-domain denoising  ·  *medium, ~40 min*

`data/noisy_image.npy` is a 256×256 image with Gaussian noise. Clean it with
an ideal low-pass filter.

* `transform_2d`, multiply by a radial mask, `inverse_2d`.
* Build the mask without `fftshift`: frequency index `k` represents the
  frequency `min(k, N−k)`, so radius² = `fy² + fx²` with those wrapped
  indices.
* Report PSNR before and after.
* Try `CUTOFF` at 20 / 42 / 90 and note the trade: too low blurs the image,
  too high keeps the noise.

---

## Expected output

| | key result |
|---|---|
| P1 | `[15, 12, −13, 27, 35, −3, −1]`, matches `np.convolve` |
| P2 | period **37** (main lobe ends at lag 9) |
| P3 | delay **300**, recovery error `5.6e−16` |
| P4 | 4226 digits, matches Python `pow` |
| P5 | found at **(148, 61)**, exact match |
| P6 | PSNR **17.25 → 21.85 dB**, keeping 8.4% of coefficients |

## Techniques covered

| technique | problem |
|---|---|
| linear convolution via zero-padding | P1 |
| autocorrelation, Wiener–Khinchin | P2 |
| cepstrum / homomorphic deconvolution | P3 |
| spectral big-integer multiplication | P4 |
| 2-D cross-correlation, separable transforms | P5 |
| spectral masking / filtering | P6 |
