# Presenter guide: the Laplace transform in 3D

15 scenes, 14:30 of animation, 151 pause points. Syllabus: Lecture 6 (`6 - Laplace.pdf`).
On screen there is deliberately little text; what to say at each pause point is below.

## How to present

- **`player.html`** (open it in Chrome, Edge or Safari): plays scene by scene and **stops at every pause point**.
  - `Space` / `→` / `PageDown` / clicker: play on to the next pause point (pressed while playing: jump straight there)
  - `←` / `PageUp`: back one pause point · `]` / `[`: next / previous scene · `Home`: restart the scene
  - `N`: talking points (hidden by default, in case your screen is mirrored) · `L`: scene list · `F`: fullscreen · `B`: black screen
- **`videos/Laplace3D_all.mp4`**: everything in one file, with a chapter marker at every pause point (VLC or IINA show them).
- **`videos/NN_Scene.mp4`**: one file per scene, if you want to drop them into slides.
- **Interactive 3D explorer** for live "what if" questions: `../interactive_3d/laplace_3d_explorer.html` (works offline)
  or the published page https://claude.ai/artifact/DaYCmbwM76a5kbFnoYBDGy. Nine views in the same order as the talk;
  `←` / `→` switch views, drag to rotate, `P` hides the side panel, `R` resets the camera.

## Running order

| # | Scene | Part | Length | Pauses |
|---|---|---|---|---|
| 00 | The big picture | What it is | 0:27 | 6 |
| 01 | Complex numbers and Euler's formula | Background | 1:49 | 16 |
| 02 | The complex exponential e^{st} | Background | 1:12 | 14 |
| 03 | Integrals and convergence | Background | 1:00 | 8 |
| 04 | Fourier recap, and where it fails | Background | 0:55 | 11 |
| 05 | How it comes up: LTI systems | How it comes up | 0:48 | 10 |
| 06 | What it is: the definition | What it is | 0:48 | 8 |
| 07 | Picturing X(s): the s-plane landscape | What it is | 0:50 | 8 |
| 08 | How it is used | How it is used | 1:06 | 12 |
| 09 | Examples 9.1 and 9.2: same X(s), different ROC | Examples | 0:54 | 7 |
| 10 | Examples 9.3, 9.4, 9.5 | Examples | 0:48 | 8 |
| 11 | ROC properties 1 to 5 | The ROC | 0:56 | 9 |
| 12 | ROC properties 6 to 8, Examples 9.7 and 9.8 | The ROC | 0:59 | 12 |
| 13 | The inverse Laplace transform | Inverse transform | 1:08 | 14 |
| 14 | Partial fractions, Examples 9.9 to 9.11 | Inverse transform | 0:44 | 8 |

## 00 · The big picture

`videos/00_BigPicture.mp4` · 0:27 · part: What it is

| At | On screen | Say |
|---|---|---|
| 0:02 | a signal in time | This is a damped oscillation, x(t) = e^(-0.5t) cos 2t for t ≥ 0. Today's question: what does the Laplace transform turn it into? |
| 0:08 | becomes a landscape over the s-plane | It becomes a function X(s) on the complex s-plane. We draw its size /X(s)/ as a height, so we get a landscape. The bright part of the floor is the region of convergence (ROC); outside it the surface is ghosted. |
| 0:13 | poles: the decay rate and the frequency | The two spikes are poles at s = -0.5 ± 2j. Their real part (-0.5) is the decay rate of x(t); their imaginary part (±2) is its frequency. Where the spikes stand tells you how the signal behaves. |
| 0:17 | Fourier is one slice of it | The yellow curve is the landscape along the jω-axis (σ = 0). That slice is /X(jω)/, the Fourier transform. Laplace keeps the whole plane; Fourier is one line of it. |
| 0:19 | the formula we will unpack | The formula we will build up to: X(s) = integral of x(t) e^(-st) dt. Every piece of it gets its own picture. |
| 0:25 | roadmap | Plan: background (complex numbers, e^(st), integrals, Fourier), where Laplace comes from (LTI systems), what it is, how it is used, the ROC, and the inverse transform. |

## 01 · Complex numbers and Euler's formula

`videos/01_ComplexToEuler.mp4` · 1:49 · part: Background

| At | On screen | Say |
|---|---|---|
| 0:02 | the complex plane | A complex number is a point, or an arrow from the origin, in a plane: horizontal = real part, vertical = imaginary part. |
| 0:05 | z = a + jb | z = a + jb: go a along the real axis and b along the imaginary axis. Engineers write j for the square root of -1. |
| 0:10 | multiply by j: rotate 90 degrees | Multiplying by j turns the arrow 90 degrees anticlockwise without changing its length. |
| 0:15 | j squared = -1 | Do it twice: 180 degrees, the arrow points the opposite way. So j times j = -1. That is what j means geometrically. |
| 0:19 | polar form: length and angle | Any arrow is also described by its length r = /z/ and its angle θ: z = r(cos θ + j sin θ). |
| 0:25 | multiplying = rotate and scale | Multiplying by w scales by /w/ and rotates by the angle of w: lengths multiply, angles add. Remember this: e^(-sτ) and H(s) later act on spirals exactly like this. |
| 0:31 | Euler's formula | e^(jθ) is the point on the unit circle at angle θ. Its horizontal shadow is cos θ and its vertical shadow is sin θ: e^(jθ) = cos θ + j sin θ. |
| 0:39 | any z = r e^{j theta} | So every complex number is z = r e^(jθ): a length times a pure rotation. |
| 0:46 | spinning as time passes | Now let the angle grow with time, θ = ωt. e^(jωt) is an arrow spinning at ω radians per second. |
| 0:57 | a helix: rotation + time | Give time its own axis. The tip traces a helix: rotation in the complex plane plus steady motion along t. |
| 1:09 | shadows: cos on the floor, sin on the wall | Look at the helix's shadows: on the floor (real part) we get cos ωt, on the back wall (imaginary part) sin ωt. Sinusoids are shadows of one spinning arrow. |
| 1:20 | omega: how fast it spins (sign = direction) | ω sets how fast it spins: bigger ω means tighter coils. A negative ω spins the other way. |
| 1:28 | two helices, opposite twist | e^(jωt) and e^(-jωt): same speed, opposite twist. |
| 1:38 | the sum stays in the real plane | Add them and halve: the yellow arrow always lies on the real axis, so the sum stays in the real plane. |
| 1:42 | side view: sin and -sin cancel | From the side, the imaginary parts are sin and -sin, and they cancel exactly. |
| 1:46 | top view: cos(omega t) | From above, the real parts agree: cos ωt = (e^(jωt) + e^(-jωt)) / 2. Real signals are pairs of opposite spirals, which is why the poles of real signals come in conjugate pairs. |

## 02 · The complex exponential e^{st}

`videos/02_ComplexExponentials.mp4` · 1:12 · part: Background

| At | On screen | Say |
|---|---|---|
| 0:04 | sigma < 0: decays | First the real exponential e^(σt). With σ < 0 it decays towards 0. |
| 0:07 | sigma = 0: constant | With σ = 0 it stays at 1. |
| 0:10 | sigma > 0: grows | With σ > 0 it grows without bound. |
| 0:19 | e^{st}: a spiral | Now make s = σ + jω complex. e^(st) = e^(σt) e^(jωt): the e^(jωt) part spins, the e^(σt) part sets the size. Together they make a spiral. |
| 0:22 | its envelope e^{sigma t} | The red funnel is the envelope e^(σt); the spiral always lies on it. |
| 0:24 | each s is one spiral | The small plane at the bottom left is the s-plane. Every point s picks out one spiral e^(st). |
| 0:27 | left of the axis: shrinks | Left of the jω-axis (σ < 0) the funnel narrows and the spiral dies out. |
| 0:31 | on the j omega-axis: spins forever | On the jω-axis (σ = 0) it is a pure helix that never decays or grows. These are Fourier's building blocks, e^(jωt). |
| 0:35 | right of the axis: grows | Right of the axis (σ > 0) the funnel widens and the spiral blows up. |
| 0:46 | omega: faster, slower, reversed | Moving up or down changes ω: faster spin, slower spin, or below the axis the spin reverses. |
| 0:50 | on the real axis: no spin | On the real axis (ω = 0) there is no spin at all, just e^(σt). |
| 0:55 | the map of the s-plane | So the s-plane is a map of every exponential behaviour: left half decays, right half grows, the jω-axis oscillates forever. |
| 1:05 | conjugate pair = damped cosine | A point s and its mirror image s* give opposite spirals; their average is the real signal e^(σt) cos ωt, a damped cosine. |
| 1:09 | seen from above: e^{sigma t} cos(omega t) | Seen from above: the damped cosine. Real oscillating signals always come from such conjugate pairs. |

## 03 · Integrals and convergence

`videos/03_IntegralsConverge.mp4` · 1:00 · part: Background

| At | On screen | Say |
|---|---|---|
| 0:10 | to infinity: the area settles at 1 | An integral adds up area. The area under e^(-t) from 0 to T grows with T but levels off at 1: the improper integral to ∞ converges. |
| 0:20 | a growing integrand: diverges | If the integrand grows, like e^(0.12t), the area keeps growing forever: the integral diverges. The Laplace transform is an integral to ∞, so convergence is the whole story. |
| 0:27 | the integrand: a shrinking spiral | Now a complex integrand: e^(-st) with s = 0.35 + 1.5j is a shrinking spiral (left). Integrating it means adding up tiny arrows. |
| 0:38 | the running total settles at 1/s | Right panel: the running total, the integral from 0 to T of e^(-st), drawn in the complex plane. Its velocity at each instant is the integrand (blue arrow). The spiral shrinks, so the steps shrink, and the path spirals into one point: 1/s. |
| 0:44 | different omega: still settles | Change ω: the limit point 1/s moves, but the path still settles. |
| 0:49 | sigma = 0: circles forever | At σ = 0 the integrand never shrinks: the running total goes round a circle forever and never settles. |
| 0:53 | sigma < 0: spirals out, diverges | With σ < 0 the steps grow and the path spirals outwards: the integral diverges. So the integral of e^(-st) from 0 to ∞ equals 1/s only when Re{s} > 0. |
| 0:57 | the size depends only on sigma | Why only σ matters: /e^(-st)/ = e^(-σt). The jω part only rotates; the size, and so convergence, is decided by σ. |

## 04 · Fourier recap, and where it fails

`videos/04_FourierRecap.mp4` · 0:55 · part: Background

| At | On screen | Say |
|---|---|---|
| 0:02 | a pulse | Recall Fourier: a signal, here a rectangular pulse, can be built out of sinusoids. |
| 0:08 | each wave slides forward and adds in | Each lane holds one cosine at frequency ω with the right amplitude. Slide them forward and add: the yellow partial sum approaches the pulse. |
| 0:16 | 13 sinusoids already make the pulse | With just 13 frequencies we already have the pulse, with ripples at the edges. |
| 0:22 | the spectrum: how much of each frequency | The heights of the waves, plotted against ω on the side wall, form the spectrum X(jω): how much of each frequency the signal contains. |
| 0:24 | and back: add them all up | Synthesis: x(t) = 1/(2π) times the integral of X(jω) e^(jωt) dω adds all the spinning arrows back together. |
| 0:30 | the waterfall from another angle | The same waterfall from another angle; for this pulse the spectrum is 2 sin(ω)/ω. |
| 0:38 | a growing spiral: the integral diverges | The problem: x(t) = e^(0.25t) u(t) grows. The Fourier integrand x(t) e^(-jωt) is a growing spiral and the integral diverges: no Fourier transform. The same happens for unstable systems. |
| 0:41 | idea: first multiply by e^{-sigma t} | Idea: first multiply by a decaying weight e^(-σt). |
| 0:45 | sigma = 0.25: just balanced | At σ = 0.25 the weight exactly cancels the growth: the spiral neither grows nor shrinks, which is still not enough to converge. |
| 0:50 | weighted enough: it converges | For σ > 0.25 the weighted integrand shrinks and the integral converges. |
| 0:52 | Fourier of the weighted signal = Laplace | The Fourier transform of the weighted signal x(t) e^(-σt) is exactly what we will call the Laplace transform X(σ + jω). |

## 05 · How it comes up: LTI systems

`videos/05_HowItComesUp.mp4` · 0:48 · part: How it comes up

| At | On screen | Say |
|---|---|---|
| 0:01 | an LTI system | An LTI system is completely described by its impulse response h(t). The output is the convolution y(t) = integral of h(τ) x(t − τ) dτ. |
| 0:05 | weights h(tau) along the tau axis | Read h(τ) (red, on the side wall) as weights: how much the input from τ seconds ago still matters now. |
| 0:09 | delayed copies x(t - tau), scaled by h(tau) | Each lane is the input delayed by τ and scaled by h(τ). |
| 0:14 | add them up: the output y(t) | Adding all the lanes gives the output y(t) in yellow. Convolution is a weighted sum of delayed copies of the input. |
| 0:21 | the input spiral | Now feed in a complex exponential e^(st), a spiral. |
| 0:25 | delay it by tau | Delay it by τ: the purple spiral e^(s(t − τ)). |
| 0:31 | same spiral, turned by omega*tau | The delayed spiral is exactly the original turned by ωτ and scaled by e^(-στ): e^(s(t − τ)) = e^(-sτ) e^(st). A delay is just multiplication by a complex number. |
| 0:39 | out comes the same spiral, times H(s) | So every delayed copy is a multiple of e^(st), and so is their weighted sum: y(t) = H(s) e^(st). The same spiral comes out, only rotated and scaled. |
| 0:42 | H(s): one complex number per s | H(s) = integral of h(τ) e^(-sτ) dτ is one complex number for each s. e^(st) is an eigenfunction of every LTI system and H(s) is its eigenvalue. |
| 0:45 | s = j omega: Fourier; any s: Laplace | On s = jω, H(jω) is the frequency response, the Fourier transform of h. For a general s it is the Laplace transform of h. That is how the Laplace transform comes up. |

## 06 · What it is: the definition

`videos/06_LaplaceDefinition.mp4` · 0:48 · part: What it is

| At | On screen | Say |
|---|---|---|
| 0:04 | the definition | Definition: X(s) = integral from -∞ to ∞ of x(t) e^(-st) dt, with s = σ + jω. We write x(t) ↔ X(s). |
| 0:09 | a Fourier transform of the weighted signal | Split e^(-st) = e^(-σt) e^(-jωt): X(σ + jω) is the Fourier transform of x(t) e^(-σt). For each σ, it is an ordinary Fourier transform of a weighted signal. |
| 0:15 | the signal grows: no Fourier transform | Take x(t) = e^(0.5t) u(t). It grows, so it has no Fourier transform. |
| 0:20 | one weighted copy per sigma | Each lane is x(t) e^(-σt) for one value of σ (the depth axis). Red lanes still grow, green lanes decay, and the grey one at σ = 0.5 is flat. |
| 0:30 | sweep sigma: the weight wins once sigma > 0.5 | Sweep σ with the yellow slice: once σ > 0.5 the weight beats the growth and the weighted signal decays. |
| 0:32 | these sigmas: the region of convergence | Those values of σ form the region of convergence: σ > 0.5. |
| 0:39 | every omega works: a half-plane | On the s-plane ω makes no difference to convergence, so the ROC is the half-plane Re{s} > 0.5. Here X(s) = 1/(s - 0.5). |
| 0:42 | Fourier = the j omega-axis, which is outside here | The jω-axis (where Fourier lives) is outside the ROC, so there is no Fourier transform, but the Laplace transform exists. That is Laplace's first advantage. |

## 07 · Picturing X(s): the s-plane landscape

`videos/07_SPlaneLandscape.mp4` · 0:50 · part: What it is

| At | On screen | Say |
|---|---|---|
| 0:02 | each s gives a complex number X(s) | Example 9.1: x(t) = e^(-t) u(t), X(s) = 1/(s + 1). At each point s, X(s) is one complex number; for example X(0.5 + j) = 0.46 - 0.31j. |
| 0:05 | its size becomes a height | Plot its size /X(s)/ as a height above that point. |
| 0:11 | the landscape /X(s)/ | Do that for every s and you get a landscape over the s-plane. |
| 0:13 | a pole: X(s) blows up at s = -1 | At s = -1 the denominator is zero and X blows up: a pole, drawn as a chimney that goes up forever (we cut it off). |
| 0:17 | only the ROC part is the transform | The ROC Re{s} > -1 is where the integral converges, so only that part is the Laplace transform. The formula 1/(s + 1) continues past it (ghosted), but the integral does not. |
| 0:25 | slice along j omega: the Fourier transform | Slice along the jω-axis: /X(jω)/ = 1/√(1 + ω²), the Fourier magnitude, projected on the back wall. The jω-axis is inside the ROC, so the Fourier transform exists. |
| 0:37 | zeros touch the floor, poles shoot up | Example 9.3: X(s) = (s - 1)/((s + 1)(s + 2)). Zeros (numerator = 0, drawn o) are where the landscape touches the floor; poles (denominator = 0, drawn x) shoot up. |
| 0:48 | seen from above: the pole-zero plot | Seen from above, the landscape becomes the pole-zero plot: the pole-zero plot is a map of this landscape. |

## 08 · How it is used

`videos/08_HowItsUsed.mp4` · 1:06 · part: How it is used

| At | On screen | Say |
|---|---|---|
| 0:13 | velocity = s times position | The velocity of e^(st) is s times its position: d/dt e^(st) = s e^(st). The yellow arrow (velocity) is the blue arrow (position) turned by the angle of s and stretched by /s/. |
| 0:15 | so d/dt becomes multiplication by s | So differentiation becomes multiplication by s: dx/dt ↔ s X(s) (bilateral transform, Lecture 7). |
| 0:20 | a mass-spring-damper style ODE | Take a second-order system, y'' + 2y' + 5y = x(t), the same shape as a mass-spring-damper. |
| 0:22 | every d/dt becomes a factor s | Transform both sides: every d/dt becomes a factor s, so s² Y + 2s Y + 5 Y = X. The differential equation is now algebra. |
| 0:25 | the system function and its poles | H(s) = Y/X = 1/(s² + 2s + 5), with poles at s = -1 ± 2j. |
| 0:33 | poles at -1 +- 2j: two spirals rise | Each pole p seeds a mode e^(pt), drawn as a spiral rising from the pole along a time axis. Left-half-plane poles give shrinking spirals. |
| 0:37 | together: a decaying oscillation h(t) | The two conjugate modes add up to the real impulse response h(t) = (1/2) e^(-t) sin 2t: a decaying oscillation. |
| 0:41 | closer to the j omega-axis: rings longer | Move the poles closer to the jω-axis: slower decay, the system rings longer (less damping). |
| 0:46 | on the axis: sustained oscillation | On the jω-axis the oscillation never dies: marginally stable. |
| 0:50 | right half-plane: unstable | In the right half-plane the response grows without bound: unstable. A causal system is stable when all its poles are in the left half-plane. |
| 0:53 | Fourier fails here, Laplace doesn't | Now h(t) grows, so it has no Fourier transform, but the Laplace transform still exists with ROC Re{s} > 0.22. Laplace can analyse unstable systems. |
| 1:03 | the toolkit | Summary: convolution becomes multiplication, differential equations become algebra, pole positions tell you stability, feedback loops become simple algebra, and all of it works for growing signals. |

## 09 · Examples 9.1 and 9.2: same X(s), different ROC

`videos/09_RightVsLeftSided.mp4` · 0:54 · part: Examples

| At | On screen | Say |
|---|---|---|
| 0:05 | the integrand spiral for t > 0 | Example 9.1: x(t) = e^(-t) u(t). The integrand x(t) e^(-st) = e^(-(s+1)t) lives on t > 0. The test point s is in the inset. |
| 0:15 | across sigma = -1 it diverges | The integrand's envelope is e^(-(σ+1)t), which shrinks only if σ > -1. Move s across σ = -1 and the spiral grows: the integral diverges. |
| 0:21 | Example 9.1: 1/(s+1), ROC right of -1 | So X(s) = 1/(s + 1) with ROC Re{s} > -1, to the right of the pole. |
| 0:30 | the integrand spiral for t < 0 | Example 9.2: x(t) = -e^(-t) u(-t), which is non-zero only for t < 0. The integrand now lives on the negative time axis. |
| 0:40 | across sigma = -1 it diverges | Now it must shrink as t goes to -∞, which needs σ + 1 < 0. Crossing σ = -1 to the right makes it diverge. |
| 0:46 | Example 9.2: 1/(s+1), ROC left of -1 | The result is X(s) = 1/(s + 1) again, but with ROC Re{s} < -1, to the left of the pole. |
| 0:52 | the ROC decides which signal you meant | Same algebraic X(s), different ROC, different signal. An X(s) without its ROC is an incomplete answer. |

## 10 · Examples 9.3, 9.4, 9.5

`videos/10_LandscapeExamples.mp4` · 0:48 · part: Examples

| At | On screen | Say |
|---|---|---|
| 0:03 | each term has its own half-plane | Example 9.3: x(t) = 3e^(-2t) u(t) - 2e^(-t) u(t). Each term has its own ROC: Re{s} > -2 and Re{s} > -1. |
| 0:06 | both must converge: Re{s} > -1 | The sum converges only where both terms converge: the intersection Re{s} > -1. X(s) = (s - 1)/((s + 1)(s + 2)). |
| 0:10 | the landscape, ROC lit | The landscape with the ROC lit. |
| 0:16 | poles at -2 and -1 +- 3j | Example 9.4: e^(-2t) u(t) + e^(-t) cos(3t) u(t). By Euler, cos 3t gives two exponentials, so the poles are -2 and -1 ± 3j (a conjugate pair, as for any real signal). The zeros are at about -1.25 ± 2.11j. |
| 0:27 | the j omega slice: resonance peaks | The ROC Re{s} > -1 contains the jω-axis, so the Fourier transform exists. The slice along jω peaks near ω = ±3 because it passes close to the poles at -1 ± 3j: that is resonance. |
| 0:36 | double zero at 1, poles at -1 and 2 | Example 9.5: δ(t) - (4/3) e^(-t) u(t) + (1/3) e^(2t) u(t). The transform of δ(t) is 1 for every s. X(s) = (s - 1)²/((s + 1)(s - 2)): poles at -1 and 2, a double zero at 1. |
| 0:39 | ROC Re{s} > 2: no Fourier transform | ROC = intersection = Re{s} > 2. The jω-axis is outside it: no Fourier transform, because the e^(2t) term grows. |
| 0:46 | far from the poles the delta leaves height 1 | Far from the poles /X(s)/ tends to 1: that constant is the δ(t) term. |

## 11 · ROC properties 1 to 5

`videos/11_ROCProperties.mp4` · 0:56 · part: The ROC

| At | On screen | Say |
|---|---|---|
| 0:06 | different omega, same envelope | Property 1: /x(t) e^(-(σ + jω)t)/ = /x(t)/ e^(-σt). Two test points with the same σ but different ω give different spirals with exactly the same envelope. |
| 0:11 | a whole vertical line converges together | So if one point on a vertical line converges, every point on that line does. |
| 0:13 | so the ROC is a union of vertical lines | The ROC is made of whole vertical lines: a vertical strip, a half-plane, or the whole plane. |
| 0:19 | poles bound the ROC | Property 2: at a pole X(s) is infinite, so the integral cannot converge there. Poles sit on ROC boundaries, never inside. |
| 0:27 | no spike at s = -1: the pole cancels | Property 3, Example 9.6: x(t) = e^(-t) on 0 < t < 2, X(s) = (1 - e^(-2(s+1)))/(s + 1). It looks like a pole at s = -1, but there 0/0 gives 2 (L'Hôpital): the landscape has height 2, no spike. |
| 0:34 | finite everywhere: big on the left, but never infinite | A finite-duration, absolutely integrable signal gives a finite integral for every s: the ROC is the entire s-plane. Instead of a pole there are zeros at s = -1 ± jπk. Big on the left, but never infinite. |
| 0:40 | the weight e^{-sigma t} over (t, sigma) | Properties 4 and 5 use the weight e^(-σt), drawn as a surface over (t, σ). |
| 0:46 | right-sided: ROC extends to the right | Right-sided signal: only t > 0 matters. There, increasing σ only lowers the weight (green slice under grey). If σ₀ converges, every σ > σ₀ converges: the ROC extends to the right. |
| 0:53 | left-sided: ROC extends to the left | Left-sided signal: only t < 0 matters, and there decreasing σ lowers the weight. The ROC extends to the left. |

## 12 · ROC properties 6 to 8, Examples 9.7 and 9.8

`videos/12_ROCStrips.mp4` · 0:59 · part: The ROC

| At | On screen | Say |
|---|---|---|
| 0:01 | Example 9.7: a two-sided signal, split in two | Example 9.7: x(t) = e^(-b/t/) is two-sided. Split it into a right part e^(-bt) u(t) (blue) and a left part e^(bt) u(-t) (red). |
| 0:05 | both ROCs overlap in a strip | Right part: ROC Re{s} > -b. Left part: ROC Re{s} < b. Both must converge, which leaves the strip -b < Re{s} < b (Property 6). |
| 0:10 | the landscape, strip lit | X(s) = -2b/(s² - b²), with poles at ±b on the edges of the strip. |
| 0:16 | smaller b: a thinner strip | Make b smaller: the signal decays more slowly and the strip gets thinner. |
| 0:21 | b <= 0: the strip is gone | For b ≤ 0 the two half-planes no longer overlap: no ROC, so no Laplace transform at all. |
| 0:26 | poles chop the plane into strips | Properties 7 and 8 (rational X(s)): ROC edges pass through poles, so the poles chop the plane into vertical strips. |
| 0:36 | the allowed ROCs | Right-sided: right of the rightmost pole. Left-sided: left of the leftmost pole. Two-sided: a strip between two poles. |
| 0:42 | two poles: -1 and -2 | Example 9.8: X(s) = 1/((s + 1)(s + 2)), poles at -1 and -2, so there are three possible ROCs. |
| 0:46 | right of both poles: right-sided | Re{s} > -1 gives the right-sided signal x(t) = (e^(-t) - e^(-2t)) u(t). |
| 0:50 | left of both poles: left-sided | Re{s} < -2 gives the left-sided signal x(t) = (-e^(-t) + e^(-2t)) u(-t). |
| 0:53 | between the poles: two-sided | -2 < Re{s} < -1 gives the two-sided signal x(t) = -e^(-t) u(-t) - e^(-2t) u(t). |
| 0:57 | the ROC picks the signal | One X(s), three signals: the ROC picks the signal. How do we compute them? That is the inverse transform. |

## 13 · The inverse Laplace transform

`videos/13_InverseLaplace.mp4` · 1:08 · part: Inverse transform

| At | On screen | Say |
|---|---|---|
| 0:01 | start from the Fourier view | Start from X(σ + jω) = Fourier transform of x(t) e^(-σt). |
| 0:03 | invert the Fourier transform | Undo the Fourier transform: x(t) e^(-σt) = 1/(2π) times the integral of X(σ + jω) e^(jωt) dω. |
| 0:05 | multiply by e^{sigma t} | Multiply both sides by e^(σt): x(t) = 1/(2π) times the integral of X(σ + jω) e^((σ + jω)t) dω. |
| 0:07 | the Bromwich integral | Substitute s = σ + jω (σ fixed, ds = j dω): x(t) = 1/(2πj) times the integral of X(s) e^(st) ds from σ - j∞ to σ + j∞. This is the Bromwich integral; σ can be anywhere inside the ROC. |
| 0:16 | the values of X(s) along the line | Geometrically: walk up the vertical line Re{s} = σ inside the ROC, reading off X(s) along the way (the yellow curve on the landscape). |
| 0:18 | each point contributes X(s) e^{st} | Each point s on the line contributes X(s) e^(st): a spiral weighted by X(s). |
| 0:26 | each wave grows like e^{sigma t}... | Numerically, as a Riemann sum: add waves at ω = kΔω. With σ = 0.3 every one of them grows like e^(0.3t)... |
| 0:33 | ...yet together they rebuild e^{-t}u(t) | ...yet together they rebuild the decaying e^(-t) u(t): the growing parts cancel. |
| 0:37 | in the limit: exactly x(t) | With all frequencies (the integral) we get exactly x(t), including the value 0.5 at the jump (the midpoint). |
| 0:46 | line right of the pole: e^{-t}u(t) | With the line to the right of the pole (σ = 0.3) the result is e^(-t) u(t). |
| 0:54 | left of the pole: -e^{-t}u(-t) | Slide the same line to the left of the pole (σ = -1.5): the very same X(s) now gives -e^(-t) u(-t). The line has to lie in the ROC, and a different ROC gives a different signal. |
| 1:00 | t > 0: enclose the pole | In practice the line is closed with a large semicircle. For t > 0 close to the left: the contour encloses the pole, and its residue gives e^(-t). |
| 1:03 | t < 0: enclose nothing | For t < 0 close to the right: nothing is inside, so x(t) = 0. That is why the result is right-sided. |
| 1:06 | the residue theorem does the integral | The Cauchy residue theorem evaluates the integral (beyond this course; the slides link a video). For rational X(s) we use partial fractions instead. |

## 14 · Partial fractions, Examples 9.9 to 9.11

`videos/14_PartialFractions.mp4` · 0:44 · part: Inverse transform

| At | On screen | Say |
|---|---|---|
| 0:01 | split into simple terms | For a rational X(s), split it into simple terms: 1/((s + 1)(s + 2)) = A/(s + 1) + B/(s + 2). |
| 0:04 | cover-up: A = 1, B = -1 | Cover-up method: A = (s + 1) X(s) at s = -1, which is 1; B = (s + 2) X(s) at s = -2, which is -1. |
| 0:07 | the expansion is always the same | So X(s) = 1/(s + 1) - 1/(s + 2), whatever the ROC. |
| 0:12 | which side of the pole is the ROC on? | Each term A/(s + a) has two possible inverses: if the ROC is to the right of its pole, A e^(-at) u(t); if to the left, -A e^(-at) u(-t). |
| 0:23 | Example 9.9: Re s > -1 | Example 9.9, ROC Re{s} > -1: right of both poles, so both terms are causal: x(t) = (e^(-t) - e^(-2t)) u(t). |
| 0:29 | Example 9.10: Re s < -2 | Example 9.10, ROC Re{s} < -2: left of both poles, so both terms are anticausal: x(t) = (-e^(-t) + e^(-2t)) u(-t). |
| 0:35 | Example 9.11: -2 < Re s < -1 | Example 9.11, -2 < Re{s} < -1: the ROC is right of -2 (causal term) but left of -1 (anticausal term): x(t) = -e^(-t) u(-t) - e^(-2t) u(t). |
| 0:41 | partial fractions + ROC = inverse transform | Recipe: expand in partial fractions, check which side of each pole the ROC is on, invert each term, add them up. |

## Re-rendering

```sh
cd manim_3d
JOBS=8 ./render_all.sh                               # everything, 1080p60
./render_all.sh -qh s07_landscape.py:SPlaneLandscape    # one scene, then rebuilds this guide and the player
```
