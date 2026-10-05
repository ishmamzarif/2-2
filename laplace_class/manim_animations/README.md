# Laplace transform animations (Manim)

3Blue1Brown-style animations for the two lecture decks in this folder
(`6 - Laplace.pdf`, `7 - More Laplace.pdf`). The visual ideas follow 3b1b's
*The Physics of Euler's Formula*, *But what is a Laplace Transform?* and
*Why Laplace transforms are so useful*.

Rendering puts the videos in `videos/` (`Lecture6_all.mp4` and `Lecture7_all.mp4` are the scenes joined back to back).
They aren't committed to the repo; see [../README.md](../README.md) for setup and rendering on macOS, Linux and Windows.

## Scenes

| # | File | Scene | Slides | What you see |
|---|------|-------|--------|--------------|
| 01 | `l6_01_exponentials.py` | `ExponentialsOnSPlane` | L6 p.2–3 | e^{st} is an eigenfunction of LTI systems; dragging s around the s-plane spins/grows/decays the spiral e^{st} |
| 02 | `l6_02_definition.py` | `LaplaceAsWeightedFourier` | L6 p.4–5 | X(σ+jω) = F{x(t)e^{−σt}}: the weight tames e^{0.5t}u(t), the ROC appears |
| 03 | `l6_02_definition.py` | `IntegralAsSpiral` | L6 p.4 | ∫e^{−st}dt as tip-to-tail vectors spiralling into 1/s, diverging when Re{s} ≤ 0 |
| 04 | `l6_03_roc.py` | `SameFormulaDifferentROC` | Ex 9.1, 9.2 | e^{−at}u(t) vs −e^{−at}u(−t): identical X(s), opposite ROCs, sweeping test line |
| 05 | `l6_03_roc.py` | `ROCProperties` | Props 1–6, Ex 9.7 | vertical strips, no poles inside, finite duration, e^{−b\|t\|} = left + right part, b ≤ 0 |
| 06 | `l6_04_poles_zeros.py` | `PoleZeroLandscape` | Ex 9.4, 9.5 | 3D \|X(s)\| landscape: poles as tent poles, zeros touching the floor, jω slice = Fourier |
| 07 | `l6_05_inverse.py` | `InverseLaplaceBuildUp` | L6 p.22–25 | Bromwich integral built up numerically; moving the line past the pole flips the answer |
| 08 | `l6_05_inverse.py` | `PartialFractionsAndROC` | Ex 9.8–9.11 | 1/((s+1)(s+2)) and its three ROCs → three different signals |
| 09 | `l7_01_properties.py` | `PropertiesOnSPlane` | L7 p.4–8 | time shift, s-shift, scaling, reversal, conjugation, shown on signal + s-plane |
| 10 | `l7_01_properties.py` | `DerivativeMeansMultiplyByS` | L7 p.10–11 | velocity of e^{st} = s × position ⇒ d/dt ↔ s; u(t) → δ(t) pole cancellation |
| 11 | `l7_01_properties.py` | `RepeatedPoles` | Ex 9.14 | t·x(t) stacks poles: 1/(s+a)^n, plus integration ↔ 1/s |
| 12 | `l7_02_convolution.py` | `ConvolutionBecomesMultiplication` | L7 p.9, p.23 | sliding convolution integral vs one multiplication in s |
| 13 | `l7_03_systems.py` | `CausalityAndStability` | Ex 9.17–9.20 | one H(s), three ROCs: causal / stable / anticausal |
| 14 | `l7_03_systems.py` | `PoleDragStability` | Ex 9.21 | drag poles across the jω-axis and watch h(t) decay, ring, or blow up |
| 15 | `l7_04_diff_eq.py` | `ODEBecomesAlgebra` | Ex 9.23, LCCDE | dy/dt + 3y = x → H(s) = 1/(s+3), solved for e^{−2t}u(t) |
| 16 | `l7_04_diff_eq.py` | `SpringMassPoles` | LCCDE | mass–spring–damper: poles move with the damping, the block moves accordingly |

## Rendering

```sh
cd laplace_class/manim_animations
source ../.venv/bin/activate                       # Windows (Git Bash): source ../.venv/Scripts/activate

manim -pql l6_02_definition.py IntegralAsSpiral   # quick preview of one scene
bash render_all.sh                                 # everything, 1080p60, into videos/
JOBS=4 bash render_all.sh -qm                      # 720p30, 4 scenes at a time
```

`common.py` holds the shared look (palette, the `SPlane` helper, ROC shading,
pole/zero markers, clipped graphs). Requirements (Manim Community 0.21, LaTeX,
ffmpeg) and how to install them are in [../README.md](../README.md).
