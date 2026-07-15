import csv 
def alu(cs2, cs1, cs0, A, B, Cin=0):
    # ---------- helpers ----------
    def bits_to_u(x):
        return int("".join(map(str, x)), 2)

    def to_signed4(x):
        return x - 16 if x & 0b1000 else x

    # ---------- inputs ----------
    A_u = bits_to_u(A)
    B_u = bits_to_u(B)
    A_s = to_signed4(A_u)
    B_s = to_signed4(B_u)

    op = (cs2, cs1, cs0)

    # ---------- operation ----------
    if op == (0,0,0):            # SUB: A - B
        B_comp = (~B_u & 0b1111) + 1
        raw = A_u + B_comp
        op_type = "SUB"

    elif op == (0,1,1):          # DEC: A - 1
        raw = A_u + 0b1111      # same as A + (-1)
        op_type = "DEC"

    elif op == (1,0,0):          # INC: A + 1
        raw = A_u + 1
        op_type = "INC"

    elif op == (1,1,1):          # ADD + Cin
        raw = A_u + B_u + Cin
        op_type = "ADD"

    elif op[1:] == (0,1):        # AND
        raw = A_u & B_u
        op_type = "LOGIC"

    elif op[1:] == (1,0):        # OR
        raw = A_u | B_u
        op_type = "LOGIC"

    else:
        raise ValueError("Unknown control signal")

    # ---------- 4-bit result ----------
    R_u = raw & 0b1111
    R_s = to_signed4(R_u)
    F = [(R_u >> i) & 1 for i in reversed(range(4))]

    # ---------- flags ----------
    # Carry / Borrow: 5th bit of raw
    if op_type in ("ADD", "INC", "DEC"):
        C = (raw >> 4) & 1  # carry-out
    elif op_type == "SUB":
        C = (raw >> 4) & 1  # 1 = no borrow, 0 = borrow
    else:
        C = 0

    # Zero flag
    Z = 1 if R_u == 0 else 0
    # Sign flag
    S = F[0]

    # Overflow flag
    V = 0
    if op_type == "ADD":
        V = int((A_s >= 0 and B_s >= 0 and R_s < 0) or
                (A_s < 0 and B_s < 0 and R_s >= 0))
    elif op_type == "SUB":
        V = int((A_s >= 0 and B_s < 0 and R_s < 0) or
                (A_s < 0 and B_s >= 0 and R_s >= 0))
    elif op_type == "INC":
        V = int(A_s == 7)
    elif op_type == "DEC":
        V = int(A_s == -8)

    return F, C, S, V, Z

def op_name(cs2, cs1, cs0):
    op = (cs2, cs1, cs0)
    if op == (0,0,0): return "SUB"
    if op == (0,1,1): return "DEC A"
    if op == (1,0,0): return "INC A"
    if op == (1,1,1): return "ADD+CIN"
    if op[1:] == (0,1): return "AND"
    if op[1:] == (1,0): return "OR"
    return "UNKNOWN"


def check_table(filename="truth_table.txt", outfile="alu_errors.txt"):
    with open(filename) as f, open(outfile, "w") as out:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        cnt = 0

        for line_no, row in enumerate(reader, start=2):
            cs2, cs1, cs0 = map(int, row[:3])
            A = list(map(int, row[3:7]))
            B = list(map(int, row[7:11]))
            # Cin = int(row[11])
            Cin = 1

            F_expected = list(map(int, row[12:16]))
            S_expected = int(row[16])
            Z_expected = int(row[17])
            V_expected = int(row[18])
            C_expected = int(row[19])

            F, Cout, S, V, Z = alu(cs2, cs1, cs0, A, B, Cin)

            if (F != F_expected or 
                S != S_expected or 
                Cout != C_expected or
                V != V_expected or 
                Z != Z_expected):

                operation = op_name(cs2, cs1, cs0)

                out.write(f"\nMismatch at line {line_no}  ({operation})\n")
                out.write(f"A: {A}\n")
                out.write(f"B: {B}\n")

                out.write("Circuit:, Equation:\n")
                out.write(f"""  F: {F_expected}  \n     {F}\n""")
                out.write(f"  S: {S_expected}, {S}\n")
                out.write(f"  C: {C_expected}, {Cout}\n")
                out.write(f"  V: {V_expected}, {V}\n")
                out.write(f"  Z: {Z_expected}, {Z}\n")

                # out.write("Equation:\n")
                # out.write(f"  F: {F}\n")
                # out.write(f"  S: {S}\n")
                # out.write(f"  V: {V}\n")
                # out.write(f"  Z: {Z}\n")

                cnt += 1

        out.write(f"\nTotal errors: {cnt}\n")

check_table()
