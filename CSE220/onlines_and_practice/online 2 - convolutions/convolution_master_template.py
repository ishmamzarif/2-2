"""
==========================================================================================
CSE220 CONVOLUTION -- MASTER PREPARATION TEMPLATE  (single-file, runnable)
==========================================================================================

HOW TO USE
    - Run from THIS folder so `from signal_lti import ...` works:
          python convolution_master_template.py
    - Every section is a self-contained function + a demo that prints results.
    - Expected outputs (from the official PDFs) are written in comments so you can self-check.
    - Plotting is OFF by default (SHOW_PLOTS). Turn it on only if a problem asks for plots;
      for verification, printing + max-abs-difference is faster and doesn't spawn windows.

------------------------------------------------------------------------------------------
PATTERN MAP  --  "which trick does this new problem want?"
------------------------------------------------------------------------------------------
    Moving average / smoothing / weights ......... build h, use FULL-OVERLAP (stock_overlap)
    Polynomial multiply / running product ........ coeff -> signal, use FULL conv (output)
    Given step response s[n] ..................... h = s - s.shift(1);  y = (Dx) * s = x * h
    Blocks: parallel (+) then series (*) ......... h_comb = h3 * (h1 + h2)
    "Superposition of many inputs" ............... SuperSignal + output_super
    "Is this system linear / time-invariant?" .... pass system as a CALLABLE to the testers
    Causal? Stable? Memoryless? .................. inspect h[n] (support / sum|h| / delta)
    Cascade vs parallel identity ................. h_series = h1 * h2 ; h_parallel = h1 + h2

------------------------------------------------------------------------------------------
signal_lti.py API CHEAT-SHEET  (the class YOU wrote -- do not redefine it, import it)
------------------------------------------------------------------------------------------
    DiscreteSignal(start, end)                # samples for n = start .. end  (END INCLUSIVE)
    s.set_value_at_time(t, v)                 # ignores t outside range (no error)
    s.get_value_at_time(t)  -> float          # returns 0 outside range
    s.shift(k)              -> new signal      # y[n] = x[n-k], range shifts by +k
    s.add(other)           -> new signal       # sample-wise over the UNION range
    s.multiply(scalar)     -> new signal       # scale every sample
    s.times() / len(s) / s.nonzero_samples(tol)
    LTISystem(h)
        .output(x)           -> FULL convolution y[n]=sum_k x[k]h[n-k], range = h+x ranges
        .output_at_time(x,n) -> single sample
        .stock_overlap(x)    -> FULL-OVERLAP only (m-n+1 samples), used for moving averages

  GOTCHAS worth remembering under exam pressure:
    * range is END-INCLUSIVE  -> loops must be  range(start, end + 1).
    * .shift() aliases .values (shares the numpy array with the original). It's safe as long
      as you don't set_value_at_time on the shifted copy. If you must mutate a shift result,
      copy it first (e.g. s.shift(k).multiply(1)).  <-- multiply makes a fresh array.
    * .output() gives FULL convolution; moving-average problems want FULL-OVERLAP -> use
      stock_overlap (or slice output[n-1 .. m-1]).
==========================================================================================
"""

import numpy as np
from signal_lti import DiscreteSignal, LTISystem

SHOW_PLOTS = False  # flip to True only when a task explicitly asks for plots


# ------------------------------------------------------------------ small shared helpers
def make_signal(start_time, values):
    """Build a DiscreteSignal from a list of values starting at start_time."""
    s = DiscreteSignal(start_time, start_time + len(values) - 1)
    for offset, v in enumerate(values):
        s.set_value_at_time(start_time + offset, v)
    return s


def fmt(values, nd=2):
    """Format a numpy array / list as comma-separated fixed-point (like the PDFs)."""
    return ", ".join(f"{float(v):.{nd}f}" for v in values)


def max_absolute_difference(a: DiscreteSignal, b: DiscreteSignal):
    """
    Largest |a[n] - b[n]| over the COMBINED range.
    NOTE: end must be max(...), and the loop must be inclusive (end + 1).
    (These two are the classic off-by-one / min-vs-max bugs -- get them right.)
    """
    start = min(a.start_time, b.start_time)
    end = max(a.end_time, b.end_time)
    mx = 0.0
    for t in range(start, end + 1):
        mx = max(mx, abs(a.get_value_at_time(t) - b.get_value_at_time(t)))
    return mx


def signals_equal(a, b, tol=1e-9):
    return max_absolute_difference(a, b) <= tol


def conv(a: DiscreteSignal, b: DiscreteSignal):
    """Convenience: full convolution a * b (impulse responses commute, so order is free)."""
    return LTISystem(b).output(a)


# ==========================================================================================
# PART 1 -- THE SEVEN SEEN PROBLEMS
# ==========================================================================================

# -------------------------------------------------------------------------- 21A: SMOOTHING
# PROBLEM (21A): Exponential smoothing of stock prices.
#   Weight alpha on the most recent day, alpha*(1-alpha) on the one before, etc.
#   Impulse response:  h[k] = alpha * (1 - alpha)^k   for k = 0..n-1  (0 elsewhere).
#   Output length = m - n + 1  -> this is a FULL-OVERLAP problem (use stock_overlap).
def solve_exponential_smoothing(price_list, n, alpha):
    prices = make_signal(0, price_list)
    h = DiscreteSignal(0, n - 1)
    for k in range(n):
        h.set_value_at_time(k, alpha * ((1 - alpha) ** k))     # k=0 is the most recent day
    return LTISystem(h).stock_overlap(prices).values

def demo_21A():
    out = solve_exponential_smoothing([10, 11, 12, 9, 10, 13, 15, 16, 17, 18], 3, 0.8)
    print("21A exp-smoothing :", fmt(out))
    # Expected: 11.68, 9.47, 9.82, 12.29, 14.40, 15.62, 16.64, 17.63


# ---------------------------------------------------------------------- 21B: MOVING AVERAGE
# PROBLEM (21B): Unweighted (UMA) and Weighted (WMA) moving averages, window n.
#   UMA: every day weight 1/n.
#   WMA: most recent day weight n, then n-1, ... normalized by n(n+1)/2.
#   Same input signal for both; only h changes. FULL-OVERLAP (stock_overlap).
def solve_moving_averages(price_list, n):
    prices = make_signal(0, price_list)

    h_uma = DiscreteSignal(0, n - 1)
    for i in range(n):
        h_uma.set_value_at_time(i, 1 / n)
    uma = LTISystem(h_uma).stock_overlap(prices).values

    h_wma = DiscreteSignal(0, n - 1)
    weight_sum = n * (n + 1) / 2
    for i in range(n):
        h_wma.set_value_at_time(i, (n - i) / weight_sum)       # i=0 most recent -> weight n
    wma = LTISystem(h_wma).stock_overlap(prices).values
    return uma, wma

def demo_21B():
    uma, wma = solve_moving_averages([1, 2, 3, 4, 5, 6, 7, 8], 4)
    print("21B UMA           :", fmt(uma))   # 2.50, 3.50, 4.50, 5.50, 6.50
    print("21B WMA           :", fmt(wma))   # 3.00, 4.00, 5.00, 6.00, 7.00
    uma2, wma2 = solve_moving_averages([5, -2, 3, 1, 0, -6, 4, -2, 1], 3)
    print("21B UMA (case2)   :", fmt(uma2))  # 2.00, 0.67, 1.33, -1.67, -0.67, -1.33, 1.00
    print("21B WMA (case2)   :", fmt(wma2))  # 1.67, 1.17, 0.83, -2.83, 0.00, -0.67, 0.50


# ------------------------------------------------------------------ 21C: POLYNOMIAL MULTIPLY
# PROBLEM (21C): Multiply two polynomials via convolution.
#   Coefficients are given HIGH-degree first. Signal index k must be the EXPONENT,
#   so reverse: signal[k] = coeff of x^k.  Product = FULL convolution (output).
#   In a real exam the inputs come from input(); here we pass lists for testing.
def solve_polynomial_multiply(poly1_hi_first, poly2_hi_first):
    d1, d2 = len(poly1_hi_first) - 1, len(poly2_hi_first) - 1
    x1 = DiscreteSignal(0, d1)
    for k in range(d1 + 1):
        x1.set_value_at_time(k, poly1_hi_first[d1 - k])
    x2 = DiscreteSignal(0, d2)
    for k in range(d2 + 1):
        x2.set_value_at_time(k, poly2_hi_first[d2 - k])

    y = LTISystem(x2).output(x1)
    degree = d1 + d2
    coeffs = [round(y.get_value_at_time(k)) for k in range(degree, -1, -1)]  # back to hi-first
    return degree, coeffs

def demo_21C():
    deg, coeffs = solve_polynomial_multiply([3, -2, 1], [2, 0, -3, 1])
    print(f"21C poly-multiply : degree {deg}, coeffs {coeffs}")
    # Expected: degree 5, coeffs [6, -4, -7, 9, -5, 1]


# ------------------------------------------------------------------- 22A: STEP RESPONSE  (*)
# PROBLEM (22A): Given the STEP response s[n] (not the impulse response), compute output.
#   Identities:  h[n] = s[n] - s[n-1]     (first difference of the step response)
#                Dx[n] = x[n] - x[n-1]    (first difference of the input)
#                y[n] = (Dx * s)[n]       == (x * h)[n]     <- these MUST match.
#   Why it works: convolution with the difference operator commutes, so Dx*s = x*Ds = x*h.
def first_difference(sig: DiscreteSignal) -> DiscreteSignal:
    """Delta sig[n] = sig[n] - sig[n-1]  (outside range treated as 0). Uses only signal ops."""
    return sig.add(sig.shift(1).multiply(-1))

def impulse_from_step_response(s: DiscreteSignal) -> DiscreteSignal:
    return first_difference(s)                          # h[n] = s[n] - s[n-1]

def output_using_step_response(x: DiscreteSignal, s: DiscreteSignal) -> DiscreteSignal:
    return LTISystem(s).output(first_difference(x))     # y = (Dx) * s

def read_signal_from_file(filename: str, INF: int = 50) -> DiscreteSignal:
    """Exam file format:  line1 = 'nstart nend',  line2 = the samples. Kept for reference."""
    sig = DiscreteSignal(-INF, INF)
    with open(filename, "r", encoding="utf-8") as f:
        nstart, nend = map(int, f.readline().split())
        vals = list(map(float, f.readline().split()))
    for i, v in enumerate(vals):
        sig.set_value_at_time(nstart + i, v)
    return sig

def demo_22A():
    # Inline example so the demo runs without the .txt files.
    s = make_signal(0, [1, 3, 6, 6, 7])          # step response
    x = make_signal(0, [2, -1, 3, 1])            # input
    h = impulse_from_step_response(s)            # -> 1, 2, 3, 0, 1
    y_s = output_using_step_response(x, s)       # via step response
    y_h = LTISystem(h).output(x)                 # via recovered impulse response
    print("22A h = Ds        :", fmt(h.values))
    print("22A outputs match :", signals_equal(y_s, y_h), " (max diff =",
          f"{max_absolute_difference(y_s, y_h):.2e})")
    if SHOW_PLOTS:
        s.plot("Step response s[n]"); h.plot("Recovered h[n]"); y_s.plot("y via step response")


# ------------------------------------------------------------- 22B: BLOCK COMBINATION  (*)
# PROBLEM (22B): x feeds h1 and h2 in PARALLEL, their sum feeds h3 in SERIES:
#       y = h3 * (h1_out + h2_out) = h3 * ((x*h1) + (x*h2))
#   Equivalent single system:  h_combined = h3 * (h1 + h2).
#   (parallel branches ADD their impulse responses; series blocks CONVOLVE.)
def solve_block_combination(x, h1, h2, h3):
    sys1, sys2, sys3 = LTISystem(h1), LTISystem(h2), LTISystem(h3)
    # Route 1: block by block
    y_blockwise = sys3.output(sys1.output(x).add(sys2.output(x)))
    # Route 2: single equivalent impulse response
    h_combined = sys3.output(h1.add(h2))                 # h3 * (h1 + h2)
    y_combined = LTISystem(h_combined).output(x)
    return y_blockwise, y_combined, h_combined

def demo_22B():
    INF = 10
    x = DiscreteSignal(-INF, INF); x.set_value_at_time(2, -1)
    h1 = DiscreteSignal(-INF, INF); h1.set_value_at_time(0, 1)
    h2 = DiscreteSignal(-INF, INF); h2.set_value_at_time(1, 0.5)
    h3 = DiscreteSignal(-INF, INF); h3.set_value_at_time(0, 1); h3.set_value_at_time(1, 1)
    y_bw, y_cb, _ = solve_block_combination(x, h1, h2, h3)
    print("22B blockwise==combined:", signals_equal(y_bw, y_cb))


# --------------------------------------------------------------- 22C: SUPERSIGNAL  (*)
# PROBLEM (22C): A SuperSignal holds several (coefficient, signal) pairs. Its "final" signal
#   is the weighted sum. output_super(SS) applies the LTI system to that combined signal.
#   (This is just linearity: T{sum c_i x_i} = sum c_i T{x_i}. Combine first, then convolve.)
class SuperSignal:
    def __init__(self):
        self.components = []            # list of (coefficient, DiscreteSignal)

    def add(self, signal: DiscreteSignal, coefficient=1.0):
        self.components.append((coefficient, signal))

    def get_final_signal(self) -> DiscreteSignal:
        coeff, sig = self.components[0]
        result = sig.multiply(coeff)
        for coeff, sig in self.components[1:]:
            result = result.add(sig.multiply(coeff))
        return result

def output_super(system: LTISystem, super_signal: SuperSignal) -> DiscreteSignal:
    return system.output(super_signal.get_final_signal())

def demo_22C():
    INF = 10
    x1 = DiscreteSignal(-INF, INF); x1.set_value_at_time(0, 1)
    x2 = DiscreteSignal(-INF, INF); x2.set_value_at_time(2, 1)
    ss = SuperSignal(); ss.add(x1, 2); ss.add(x2, -1)          # x = 2*x1 - x2
    h = DiscreteSignal(-INF, INF); h.set_value_at_time(0, 1); h.set_value_at_time(1, 0.5)
    system = LTISystem(h)
    y = output_super(system, ss)
    # cross-check against linearity applied the long way
    y_long = system.output(x1).multiply(2).add(system.output(x2).multiply(-1))
    print("22C output_super ok    :", signals_equal(y, y_long))


# ------------------------------------------------------------- 23A: PROPERTY TESTERS  (*)
# PROBLEM (23A): Write GENERIC testers that take a system as a CALLABLE (DiscreteSignal ->
#   DiscreteSignal). They must NOT assume the callable is an LTISystem.
#     Linearity:        max| T{a*x1 + b*x2}  -  ( a*T{x1} + b*T{x2} ) |
#     Time-invariance:  max| T{x(n-k)}       -  ( T{x}(n-k) )         |
#   A system is LTI only if BOTH are ~0.  Key insight for the "which property fails?" part:
#   y[n] = n*x[n] is LINEAR (n factors out) but TIME-VARYING -> fails time-invariance ONLY.
def test_linearity(apply_system, x1, x2, a, b):
    lhs = apply_system(x1.multiply(a).add(x2.multiply(b)))            # T{a x1 + b x2}
    rhs = apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))  # a T{x1} + b T{x2}
    return max_absolute_difference(lhs, rhs)

def test_time_invariance(apply_system, x, k):
    lhs = apply_system(x.shift(k))       # T{x(n-k)}
    rhs = apply_system(x).shift(k)       # y(n-k)
    return max_absolute_difference(lhs, rhs)

def demo_23A():
    x1 = make_signal(-2, [1, 0, 2, -1, 3])
    x2 = make_signal(-1, [2, -3, 0, 1, 1])
    a, b, k = 2.0, -3.0, 3

    # System A: genuine LTI via impulse response h -> both tests ~0
    h = make_signal(0, [1.0, 0.5, 0.25])
    sysA = LTISystem(h)
    print("23A SystemA linearity  :", f"{test_linearity(sysA.output, x1, x2, a, b):.2e}")
    print("23A SystemA time-inv   :", f"{test_time_invariance(sysA.output, x1, k):.2e}")

    # System B: y[n] = n*x[n]  -> linearity ~0, time-invariance NONZERO
    print("23A SystemB linearity  :", f"{test_linearity(SYS_TIME_VARYING_GAIN, x1, x2, a, b):.2e}",
          "(=0 -> LINEAR)")
    print("23A SystemB time-inv   :", f"{test_time_invariance(SYS_TIME_VARYING_GAIN, x2, k):.2e}",
          "(!=0 -> FAILS time-invariance)")
    print("23A conclusion         : System B fails TIME-INVARIANCE only (it is linear).")


# ==========================================================================================
# PART 2 -- PREDICTED PROBLEMS  (emphasis: PROPERTY TESTS & SYSTEM TYPES + SYSTEM COMBINATIONS)
# ==========================================================================================

# --------------------------------------------------------- A LIBRARY OF EXAMPLE SYSTEMS
# Each is a plain callable DiscreteSignal -> DiscreteSignal, ready to drop into the 23A testers.
# Comment tags: [L]=linear [NL]=nonlinear [TI]=time-invariant [TV]=time-varying
#               [C]=causal [NC]=non-causal [M]=memoryless [S]=BIBO-stable

def SYS_AMPLIFIER(c):                       # y[n] = c*x[n]              [L][TI][C][M][S]
    return lambda x: x.multiply(c)

def SYS_DELAY(d):                           # y[n] = x[n-d]             [L][TI][C if d>=0][S]
    return lambda x: x.shift(d)

def SYS_TIME_VARYING_GAIN(x):               # y[n] = n*x[n]             [L][TV] (23A's System B)
    y = DiscreteSignal(x.start_time, x.end_time)
    for n in range(x.start_time, x.end_time + 1):        # END-INCLUSIVE loop!
        y.set_value_at_time(n, n * x.get_value_at_time(n))
    return y

def SYS_SQUARER(x):                         # y[n] = x[n]^2             [NL][TI][C][M][S]
    y = DiscreteSignal(x.start_time, x.end_time)
    for n in range(x.start_time, x.end_time + 1):
        v = x.get_value_at_time(n)
        y.set_value_at_time(n, v * v)
    return y

def SYS_TIME_REVERSAL(x):                   # y[n] = x[-n]              [L][TV][NC]
    y = DiscreteSignal(-x.end_time, -x.start_time)
    for n in range(x.start_time, x.end_time + 1):
        y.set_value_at_time(-n, x.get_value_at_time(n))
    return y

def SYS_ACCUMULATOR(x):                     # y[n] = sum_{m<=n} x[m]    [L][TI][C] (not BIBO-stable in general)
    # CAVEAT: theoretically LINEAR + TI. But this finite-range version clips the running total
    # to x's own end_time, so the classifier below reports "nonlinear" -- that is an ARTIFACT of
    # the truncated output range, NOT real nonlinearity. Lesson: make your output range wide
    # enough (here the accumulator's tail should persist past x.end_time) or the test lies.
    y = DiscreteSignal(x.start_time, x.end_time)
    running = 0.0
    for n in range(x.start_time, x.end_time + 1):
        running += x.get_value_at_time(n)
        y.set_value_at_time(n, running)
    return y

def SYS_FIRST_DIFFERENCE(x):                # y[n] = x[n]-x[n-1]        [L][TI][C]
    return x.add(x.shift(1).multiply(-1))

def SYS_ADD_CONSTANT(c):                    # y[n] = x[n]+c             [NL: affine, not linear][TI]
    def f(x):
        y = DiscreteSignal(x.start_time, x.end_time)
        for n in range(x.start_time, x.end_time + 1):
            y.set_value_at_time(n, x.get_value_at_time(n) + c)
        return y
    return f


# ------------------------------------------------ PREDICTED 1: full LTI property classifier
# PROBLEM: given ANY callable system, empirically decide linear? time-invariant? -> LTI?
#   (Empirical test with a couple of probe signals; enough to catch the usual exam systems.)
def classify_system(name, apply_system, tol=1e-9):
    x1 = make_signal(-2, [1, 0, 2, -1, 3])
    x2 = make_signal(-1, [2, -3, 0, 1, 1])
    lin = test_linearity(apply_system, x1, x2, 2.0, -3.0)
    ti = test_time_invariance(apply_system, x1, 3)
    is_lin, is_ti = lin <= tol, ti <= tol
    verdict = "LTI" if (is_lin and is_ti) else \
              ("LINEAR but TIME-VARYING" if is_lin else
               ("NONLINEAR but TIME-INVARIANT" if is_ti else "NONLINEAR & TIME-VARYING"))
    print(f"  {name:<22} lin={lin:.1e} ti={ti:.1e} -> {verdict}")

def demo_pred_classify():
    print("PREDICTED-1 classify systems:")
    classify_system("amplifier(3)",      SYS_AMPLIFIER(3))
    classify_system("delay(2)",          SYS_DELAY(2))
    classify_system("n*x[n]",            SYS_TIME_VARYING_GAIN)
    classify_system("x[n]^2",            SYS_SQUARER)
    classify_system("x[-n] reversal",    SYS_TIME_REVERSAL)
    classify_system("accumulator",       SYS_ACCUMULATOR)
    classify_system("first difference",  SYS_FIRST_DIFFERENCE)
    classify_system("x[n]+5 (affine)",   SYS_ADD_CONSTANT(5))
    print("  NOTE: accumulator is truly LINEAR+TI; its 'nonlinear' verdict is a finite-range")
    print("        artifact (the running-total tail past x.end_time is clipped). x[n]+5 is")
    print("        genuinely nonlinear (an affine offset breaks scaling: T{0} = 5 != 0).")


# --------------------------------- PREDICTED 2: causality / stability / memoryless from h[n]
# PROBLEM: For an LTI system defined by impulse response h[n], decide the standard properties.
#   Causal      <=>  h[n] = 0 for all n < 0
#   BIBO stable <=>  sum_n |h[n]| < infinity   (for finite h it's always finite -> stable)
#   Memoryless  <=>  h[n] = 0 for all n != 0   (h is a scaled impulse c*delta[n])
def analyze_impulse_response(h: DiscreteSignal, tol=1e-12):
    causal = all(abs(h.get_value_at_time(n)) <= tol
                 for n in range(h.start_time, 0) if n < 0)
    abs_sum = sum(abs(h.get_value_at_time(n)) for n in range(h.start_time, h.end_time + 1))
    memoryless = all(abs(h.get_value_at_time(n)) <= tol
                     for n in range(h.start_time, h.end_time + 1) if n != 0)
    return {"causal": causal, "abs_sum": abs_sum, "bibo_stable": np.isfinite(abs_sum),
            "memoryless": memoryless}

def demo_pred_h_properties():
    print("PREDICTED-2 impulse-response properties:")
    cases = {
        "h=delta (memoryless)": make_signal(0, [1]),
        "h=[1,0.5,0.25] causal": make_signal(0, [1, 0.5, 0.25]),
        "h non-causal (starts -1)": make_signal(-1, [0.5, 1, 0.5]),
    }
    for name, h in cases.items():
        info = analyze_impulse_response(h)
        print(f"  {name:<26} causal={info['causal']} stable={info['bibo_stable']} "
              f"sum|h|={info['abs_sum']:.3f} memoryless={info['memoryless']}")


# ------------------------------------- PREDICTED 3: cascade (series) vs parallel identities
# PROBLEM: Prove the two fundamental LTI-combination identities with your own classes:
#   SERIES  (x -> h1 -> h2):   equivalent h = h1 * h2   (convolution; order doesn't matter)
#   PARALLEL(x -> h1 & h2, summed): equivalent h = h1 + h2
def demo_pred_combinations():
    print("PREDICTED-3 system-combination identities:")
    x = make_signal(0, [1, -2, 3, 0, 1])
    h1 = make_signal(0, [1, 0.5])
    h2 = make_signal(0, [1, -1, 0.25])

    # SERIES: cascade output must equal output of (h1 * h2)
    cascade = LTISystem(h2).output(LTISystem(h1).output(x))
    h_series = conv(h1, h2)
    print("  series  cascade == (h1*h2)  :", signals_equal(cascade, LTISystem(h_series).output(x)))
    print("  series  h1*h2   == h2*h1    :", signals_equal(conv(h1, h2), conv(h2, h1)))  # commutative

    # PARALLEL: summed branches must equal output of (h1 + h2)
    parallel = LTISystem(h1).output(x).add(LTISystem(h2).output(x))
    h_parallel = h1.add(h2)
    print("  parallel sum   == (h1+h2)   :", signals_equal(parallel, LTISystem(h_parallel).output(x)))

    # ASSOCIATIVITY of cascade: (h1*h2)*h3 == h1*(h2*h3)
    h3 = make_signal(0, [2, 1])
    print("  assoc (h1*h2)*h3==h1*(h2*h3):", signals_equal(conv(conv(h1, h2), h3),
                                                            conv(h1, conv(h2, h3))))


# ------------------------------------- PREDICTED 4: cross-correlation & echo (bonus, common)
# PROBLEM: Cross-correlation r_xy[l] = sum_n x[n]*y[n+l]  ==  convolution of x with FLIPPED y.
#   Flip: y_flip[n] = y[-n]  (== SYS_TIME_REVERSAL).  Then r = x * y_flip.
#   Echo/reverb: h = delta[n] + a*delta[n-D]  (direct sound + one delayed, attenuated copy).
def cross_correlation(x, y):
    return LTISystem(SYS_TIME_REVERSAL(y)).output(x)

def echo_impulse_response(delay_D, attenuation_a, INF=20):
    h = DiscreteSignal(0, delay_D)
    h.set_value_at_time(0, 1.0)                 # direct path
    h.set_value_at_time(delay_D, attenuation_a) # delayed echo
    return h

def demo_pred_corr_echo():
    print("PREDICTED-4 correlation & echo:")
    x = make_signal(0, [1, 2, 3])
    r = cross_correlation(x, x)                 # autocorrelation, peak at lag 0
    peak_lag = max(range(r.start_time, r.end_time + 1),
                   key=lambda n: r.get_value_at_time(n))
    print("  autocorr peak lag (expect 0):", peak_lag, " values:", fmt(r.values))
    echo = LTISystem(echo_impulse_response(2, 0.6)).output(make_signal(0, [1, 0, 0, 0]))
    print("  echo of a click            :", fmt(echo.values))


# ==========================================================================================
def main():
    print("========== SEEN PROBLEMS ==========")
    # demo_21A(); demo_21B(); demo_21C(); demo_22A(); demo_22B(); demo_22C(); demo_23A()
    print("\n========== PREDICTED PROBLEMS ==========")
    demo_pred_classify()
    demo_pred_h_properties()
    demo_pred_combinations()
    demo_pred_corr_echo()


if __name__ == "__main__":
    main()
