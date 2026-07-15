#!/usr/bin/env python3
"""
Hardware-level floating-point adder - Simplified (No Sticky Bit).
Format: 1 sign bit, 4 exponent bits, 11 fraction bits.
Refactored:
1. Rounding logic extracted to function.
2. Sticky bit accumulation removed (simple truncation).
"""

import random
import sys

# -------- Configuration --------
N = 100000
EXP_BITS = 4
FRAC_BITS = 11
TOTAL_BITS = 1 + EXP_BITS + FRAC_BITS
BIAS = 7
OUT_FILE = "test_vector_gemini.txt"
# -------------------------------

def generate_random_float():
    """Generate random normalized float."""
    sign = random.randint(0, 1)
    exponent = random.randint(1, (1 << EXP_BITS) - 2)
    fraction = random.randint(0, (1 << FRAC_BITS) - 1)
    return sign, exponent, fraction

def perform_rounding(man, exp):
    """
    Applies Round-to-Nearest logic and handles post-rounding overflow.
    Input: man (shifted by 4 extra bits), exp
    Returns: rounded_man, rounded_exp
    """
    # GRS bit positions based on << 4 shift:
    # Bit 0-1: Precision bits (formerly sticky territory)
    # Bit 2:   Round (R)
    # Bit 3:   Guard (G)
    # Bit 4:   LSB of Fraction (M)

    # Simplified rounding decision (Round to Nearest)
    # We check the Guard bit (bit 3). 
    # If G is 0: Round down (do nothing)
    # If G is 1: Check R or lower bits.
    
    g_bit = (man >> 3) & 1
    r_bit = (man >> 2) & 1
    lower_bits = (man & 0x3) # Bits 0 and 1
    m_bit = (man >> 4) & 1
    
    # Logic: Round up if G=1 AND (R=1 OR Lower!=0 OR M=1 [for ties])
    # Note: Without sticky accumulation, 'lower_bits' are just 0 unless shift was small.
    round_up = g_bit and (r_bit or lower_bits or m_bit)

    # Shift back to remove the 4 extra bits
    man >>= 4
    
    if round_up:
        man += 1

    # --- Post-Rounding Normalization ---
    # If rounding caused overflow (e.g. 11.11 -> 100.00)
    if man >= (1 << (FRAC_BITS + 1)):
        man >>= 1
        exp += 1
        
    return man, exp

def add_floats_hardware(a_sign, a_exp, a_frac, b_sign, b_exp, b_frac):
    MAX_EXP = (1 << EXP_BITS) - 1
    
    # --- 1. Special Cases: Zeros ---
    if a_exp == 0 and a_frac == 0: return b_sign, b_exp, b_frac, 0, 0
    if b_exp == 0 and b_frac == 0: return a_sign, a_exp, a_frac, 0, 0

    # --- 2. Unpack & Hidden Bit ---
    a_h = 1 if a_exp > 0 else 0
    b_h = 1 if b_exp > 0 else 0
    
    a_m = (a_h << FRAC_BITS) | a_frac
    b_m = (b_h << FRAC_BITS) | b_frac
    
    a_e_eff = a_exp - BIAS if a_exp > 0 else 1 - BIAS
    b_e_eff = b_exp - BIAS if b_exp > 0 else 1 - BIAS

    # --- 3. Align Exponents ---
    if a_e_eff >= b_e_eff:
        res_exp = a_e_eff
        shift = a_e_eff - b_e_eff
        m_big, m_small = a_m, b_m
        res_sign, op = a_sign, a_sign ^ b_sign
    else:
        res_exp = b_e_eff
        shift = b_e_eff - a_e_eff
        m_big, m_small = b_m, a_m
        res_sign, op = b_sign, a_sign ^ b_sign

    # --- 4. Shift (Alignment) ---
    # Move to extended precision space (4 extra bits)
    m_big <<= 4
    m_small <<= 4

    # REMOVED: Sticky bit logic. Just simple truncation.
    if shift > 0:
        m_small >>= shift 

    # --- 5. Arithmetic ---
    if op == 0:
        res_m = m_big + m_small
    else:
        res_m = m_big - m_small
        if res_m < 0:
            res_m = -res_m
            res_sign ^= 1
    
    if res_m == 0: return 0, 0, 0, 0, 0

    # --- 6. Normalization (Pre-Rounding) ---
    target_pos = FRAC_BITS + 4
    
    # Overflow check
    if res_m >= (1 << (target_pos + 1)):
        res_m >>= 1 # REMOVED: Sticky collection here too
        res_exp += 1
    # Underflow check
    else:
        while res_m > 0 and not (res_m & (1 << target_pos)) and (res_exp + BIAS) > 0:
            res_m <<= 1
            res_exp -= 1

    # --- 7. Rounding ---
    # Reusing the extracted function
    res_m, res_exp = perform_rounding(res_m, res_exp)

    # --- 8. Packing & Exceptions ---
    final_exp_biased = res_exp + BIAS
    
    if final_exp_biased >= MAX_EXP:
        return res_sign, MAX_EXP, 0, 1, 0 # Overflow
    
    if final_exp_biased <= 0:
        return res_sign, 0, 0, 0, 1 # Underflow

    final_frac = res_m & ((1 << FRAC_BITS) - 1)
    return res_sign, final_exp_biased, final_frac, 0, 0

# --- Boilerplate Utilities ---

def bits_to_list(sign, exp, frac):
    bits = [sign]
    bits += [(exp >> i) & 1 for i in range(EXP_BITS - 1, -1, -1)]
    bits += [(frac >> i) & 1 for i in range(FRAC_BITS - 1, -1, -1)]
    return bits

def generate_samples(n):
    samples = []
    while len(samples) < n:
        a = generate_random_float()
        b = generate_random_float()
        s = add_floats_hardware(*a, *b)
        # Filter purely invalid/inf results for cleaner test vectors
        if s[1] == 0 or s[1] == (1 << EXP_BITS) - 1: continue
        
        row = bits_to_list(*a) + ['x'] + bits_to_list(*b) + ['x'] + \
              [s[3], s[4]] + ['x'] + bits_to_list(s[0], s[1], s[2])
        samples.append(row)
    return samples

def write_to_file(filename, samples):
    headers = [f'a{i}' for i in range(TOTAL_BITS-1,-1,-1)] + ['x'] + \
              [f'b{i}' for i in range(TOTAL_BITS-1,-1,-1)] + ['x', 'Ov', 'Un', 'x'] + \
              [f'S{i}' for i in range(TOTAL_BITS-1,-1,-1)]
    with open(filename, 'w') as f:
        f.write('\t'.join(headers) + '\n')
        for s in samples: f.write('\t'.join(map(str, s)) + '\n')

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else N
    samples = generate_samples(n)
    write_to_file(OUT_FILE, samples)
    print(f"No-Sticky Version: {len(samples)} samples written to {OUT_FILE}")

if __name__ == '__main__':
    main()