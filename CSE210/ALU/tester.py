"""
4-bit ALU (Group 2) truth-table tester for Logisim exports.

Usage:
    python alu_truth_table_tester.py truth_table.txt

Expected columns (Logisim Combinational Analysis -> Export Table as .txt):
    Cs2 Cs1 Cs0 | A3 A2 A1 A0 | B3 B2 B1 B0 || Z C V S Co F3 F2 F1 F0

Group 2 operations (Cin = Cs0):
    cs2 cs1 cs0 | operation        | model
    ------------|------------------|---------------------------
     0   0   0  | Sub with borrow  | A + ~B + 0  = A - B - 1
     0   0   1  | Sub              | A + ~B + 1  = A - B
     1   0   0  | Add              | A +  B + 0  = A + B
     1   0   1  | Transfer A       | A + 1111 + 1 = A
     X   1   0  | XOR              | A ^ B
     X   1   1  | AND              | A & B

Flag model (edit ASSUMPTIONS below if your design differs):
    F  : 4-bit result
    Z  : 1 if F == 0000
    S  : F3 (sign bit)
    Co : raw carry out of the 4-bit adder (bit 4 of A + Y + Cin)
    C  : carry flag. For subtraction, many designs invert Co so that
         C=1 means "borrow occurred". Default here: C = Co (change below).
    V  : signed overflow = carry_into_bit3 XOR carry_out_of_bit3
"""

import sys

# ------------------------- ASSUMPTIONS (edit me) -------------------------
C_IS_INVERTED_ON_SUB = False   # True if C = NOT Co for sub ops (borrow flag)
CHECK_FLAGS_ON_LOGIC_OPS = {   # which flags to verify when cs1 = 1 (XOR/AND)
    "Z": True, "S": True,
    "C": False, "V": False, "Co": False,   # often don't-care for logic ops
}
# --------------------------------------------------------------------------

INPUT_COLS = ["Cs2", "Cs1", "Cs0", "A3", "A2", "A1", "A0", "B3", "B2", "B1", "B0"]
OUTPUT_COLS = ["Z", "C", "V", "S", "Co", "F3", "F2", "F1", "F0"]


def expected(cs2, cs1, cs0, a, b):
    """Return dict of expected outputs for Group 2. a, b are 0..15 ints."""
    is_logic = cs1 == 1
    if is_logic:
        f = (a ^ b) if cs0 == 0 else (a & b)
        co = 0  # don't-care in most designs; not checked by default
        v = 0
        c = 0
    else:
        # arithmetic: adder computes A + Y + Cin, Cin = cs0
        if cs2 == 0:
            y = (~b) & 0xF                 # sub / sub-with-borrow
        else:
            y = b if cs0 == 0 else 0xF     # add / transfer A
        total = a + y + cs0
        f = total & 0xF
        co = (total >> 4) & 1
        # carry into bit 3 (for overflow): sum of low 3 bits + cin
        c3 = ((a & 7) + (y & 7) + cs0) >> 3 & 1
        v = c3 ^ co
        is_sub = cs2 == 0
        c = (co ^ 1) if (C_IS_INVERTED_ON_SUB and is_sub) else co
    return {
        "F3": (f >> 3) & 1, "F2": (f >> 2) & 1, "F1": (f >> 1) & 1, "F0": f & 1,
        "Z": 1 if f == 0 else 0,
        "S": (f >> 3) & 1,
        "Co": co, "C": c, "V": v,
        "_is_logic": is_logic,
    }


def parse_logisim(path):
    """Parse a Logisim combinational-analysis exported table (.txt)."""
    rows = []
    header = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or set(line) <= set("~-|+= "):
                continue  # separator lines
            tokens = [t for t in line.replace("|", " ").split() if t]
            if header is None:
                header = tokens
                continue
            if all(t in "01xX" for t in tokens):
                rows.append(tokens)
    if header is None:
        sys.exit("Could not find a header row in the file.")
    missing = [c for c in INPUT_COLS + OUTPUT_COLS if c not in header]
    if missing:
        sys.exit(f"Missing columns in file: {missing}\nFound header: {header}")
    idx = {c: header.index(c) for c in header}
    return idx, rows


def bits_to_int(bits):
    v = 0
    for b in bits:
        v = (v << 1) | b
    return v


OP_NAMES = {
    (0, 0, 0): "SUB w/ borrow (A-B-1)",
    (0, 0, 1): "SUB (A-B)",
    (1, 0, 0): "ADD (A+B)",
    (1, 0, 1): "TRANSFER A",
}


def op_name(cs2, cs1, cs0):
    if cs1 == 1:
        return "XOR" if cs0 == 0 else "AND"
    return OP_NAMES[(cs2, cs1, cs0)]


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python {sys.argv[0]} <logisim_exported_table.txt>")
    idx, rows = parse_logisim(sys.argv[1])

    total = passed = 0
    fail_by_col = {c: 0 for c in OUTPUT_COLS}
    failures = []

    for tokens in rows:
        def val(col):
            t = tokens[idx[col]]
            return None if t in "xX" else int(t)

        cs2, cs1, cs0 = val("Cs2"), val("Cs1"), val("Cs0")
        a = bits_to_int([val("A3"), val("A2"), val("A1"), val("A0")])
        b = bits_to_int([val("B3"), val("B2"), val("B1"), val("B0")])
        exp = expected(cs2, cs1, cs0, a, b)

        row_ok = True
        diffs = []
        for col in OUTPUT_COLS:
            if exp["_is_logic"] and not CHECK_FLAGS_ON_LOGIC_OPS.get(col, True):
                continue
            got = val(col)
            if got is not None and got != exp[col]:
                row_ok = False
                fail_by_col[col] += 1
                diffs.append(f"{col}: got {got}, expected {exp[col]}")
        total += 1
        if row_ok:
            passed += 1
        elif len(failures) < 50:
            failures.append(
                f"cs={cs2}{cs1}{cs0} [{op_name(cs2, cs1, cs0):22s}] "
                f"A={a:2d} ({a:04b})  B={b:2d} ({b:04b})  ->  " + "; ".join(diffs)
            )

    print(f"Rows checked : {total}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {total - passed}")
    if total - passed:
        print("\nFailures per output column:")
        for col, n in fail_by_col.items():
            if n:
                print(f"  {col:3s}: {n}")
        print(f"\nFirst {len(failures)} failing rows:")
        for f in failures:
            print("  " + f)
        print("\nHint: if ONLY C fails on SUB ops, try C_IS_INVERTED_ON_SUB = True.")
        print("Hint: if flags fail only on XOR/AND rows, adjust CHECK_FLAGS_ON_LOGIC_OPS.")
    else:
        print("\nAll rows match. Your ALU truth table is correct ✓")


if __name__ == "__main__":
    main()