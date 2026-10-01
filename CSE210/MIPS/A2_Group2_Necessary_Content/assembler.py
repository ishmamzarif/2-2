#!/usr/bin/env python3
"""
Assembler for the CSE 210 (Jan 2026) 4-bit MIPS  --  Section A2, Group 2
Opcode sequence: JOCMGNDHFIELKBAP

Usage:
    python assembler.py program.asm                 -> writes program.hex
    python3 assembler.py ex.asm -o ex.hex      -> custom output name

The output file is a Logisim ROM image ("v2.0 raw"). In Logisim,
right-click the Instruction ROM -> Load Image... and pick the file.
A human-readable listing is printed to the terminal.
"""
import re
import sys

# ---------------------------------------------------------------- opcodes
OPCODES = {
    "srl": 0x0, "bneq": 0x1, "sub": 0x2, "sw": 0x3,
    "or": 0x4, "beq": 0x5, "subi": 0x6, "ori": 0x7,
    "andi": 0x8, "sll": 0x9, "and": 0xA, "lw": 0xB,
    "nor": 0xC, "addi": 0xD, "add": 0xE, "j": 0xF,
}
R_TYPE = {"add", "sub", "and", "or", "nor"}          # op rs1 rs2 rd
S_TYPE = {"sll", "srl"}                              # op rs  rd  shamt
I_ARITH = {"addi", "subi", "andi", "ori"}            # op rs  rd  imm
MEMORY = {"lw", "sw"}                                # op base rt offset
BRANCH = {"beq", "bneq"}                             # op rs  rt  offset
JUMP = {"j"}                                         # op addr8 0000

REGISTERS = {
    "$zero": 0, "$0": 0,
    "$t0": 1, "$t1": 2, "$t2": 3, "$t3": 4, "$t4": 5,
    "$sp": 6,
}
SP = 6


class AsmError(Exception):
    pass


def parse_int(text, line_no):
    try:
        return int(text.strip(), 0)
    except ValueError:
        raise AsmError(f"line {line_no}: '{text}' is not a number")


def reg(text, line_no):
    name = text.strip().lower()
    if name not in REGISTERS:
        raise AsmError(f"line {line_no}: unknown register '{text}'")
    return REGISTERS[name]


def split_args(rest):
    return [a.strip() for a in rest.split(",")] if rest.strip() else []


def expand_pseudo(mnemonic, args, line_no):
    """push/pop become two real instructions each."""
    if mnemonic == "push":
        if len(args) != 1:
            raise AsmError(f"line {line_no}: push needs one register")
        return [("subi", ["$sp", "$sp", "1"]), ("sw", [args[0], "0($sp)"])]
    if mnemonic == "pop":
        if len(args) != 1:
            raise AsmError(f"line {line_no}: pop needs one register")
        return [("lw", [args[0], "0($sp)"]), ("addi", ["$sp", "$sp", "1"])]
    return [(mnemonic, args)]


def first_pass(source):
    """Strip comments, collect labels, expand pseudo-instructions."""
    labels, program = {}, []
    for line_no, raw in enumerate(source.splitlines(), start=1):
        line = re.split(r"#|//|;", raw, maxsplit=1)[0].strip()
        while ":" in line:                                   # one or more labels
            label, line = line.split(":", 1)
            label = label.strip()
            if not re.fullmatch(r"[A-Za-z_]\w*", label):
                raise AsmError(f"line {line_no}: bad label '{label}'")
            if label in labels:
                raise AsmError(f"line {line_no}: label '{label}' defined twice")
            labels[label] = len(program)
            line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        mnemonic = parts[0].lower()
        args = split_args(parts[1] if len(parts) > 1 else "")
        for m, a in expand_pseudo(mnemonic, args, line_no):
            program.append((m, a, line_no, raw.strip()))
    return labels, program


def layout(label_idx, program):
    """Assign addresses. A branch to a label more than -8..+7 away is
    'relaxed' into two instructions:  (inverse branch over next) + j label.
    Relaxing one branch moves later code, so repeat until nothing changes."""
    far = set()
    while True:
        addr, pc = [], 0
        for i in range(len(program)):
            addr.append(pc)
            pc += 2 if i in far else 1
        addr.append(pc)                                      # label at end of file
        labels = {name: addr[i] for name, i in label_idx.items()}
        changed = False
        for i, (mnemonic, args, _, _) in enumerate(program):
            if mnemonic in BRANCH and i not in far and len(args) == 3 and args[2] in labels:
                offset = labels[args[2]] - (addr[i] + 1)
                if not -8 <= offset <= 7:
                    far.add(i)
                    changed = True
        if not changed:
            return labels, far


def encode(mnemonic, args, pc, labels, line_no):
    if mnemonic not in OPCODES:
        raise AsmError(f"line {line_no}: unknown instruction '{mnemonic}'")
    op = OPCODES[mnemonic]

    def need(n):
        if len(args) != n:
            raise AsmError(f"line {line_no}: {mnemonic} expects {n} operands")

    if mnemonic in R_TYPE:                       # add rd, rs1, rs2
        need(3)
        rd, rs1, rs2 = (reg(a, line_no) for a in args)
        if SP in (rd, rs1, rs2):
            raise AsmError(f"line {line_no}: $sp can only be used with addi/subi/lw/sw")
        return (op << 12) | (rs1 << 8) | (rs2 << 4) | rd

    if mnemonic in S_TYPE:                       # sll rd, rs, shamt
        need(3)
        rd, rs = reg(args[0], line_no), reg(args[1], line_no)
        shamt = parse_int(args[2], line_no)
        if not 0 <= shamt <= 15:
            raise AsmError(f"line {line_no}: shamt must be 0..15")
        return (op << 12) | (rs << 8) | (rd << 4) | shamt

    if mnemonic in I_ARITH:                      # addi rd, rs, imm
        need(3)
        rd, rs = reg(args[0], line_no), reg(args[1], line_no)
        imm = parse_int(args[2], line_no)
        if SP in (rd, rs):
            if not (rd == SP and rs == SP and mnemonic in ("addi", "subi")):
                raise AsmError(f"line {line_no}: only 'addi/subi $sp, $sp, k' may touch $sp")
            if imm < 0:                          # SP immediates are zero-extended
                mnemonic, imm = ("subi" if mnemonic == "addi" else "addi"), -imm
                op = OPCODES[mnemonic]
            if not 0 <= imm <= 15:
                raise AsmError(f"line {line_no}: $sp step must be 0..15")
        elif not -8 <= imm <= 15:
            raise AsmError(f"line {line_no}: immediate must fit in 4 bits (-8..15)")
        return (op << 12) | (rs << 8) | (rd << 4) | (imm & 0xF)

    if mnemonic in MEMORY:                       # lw rt, off(base)
        need(2)
        rt = reg(args[0], line_no)
        m = re.fullmatch(r"\s*(-?\w*)\s*\(\s*(\$\w+)\s*\)\s*", args[1])
        if not m:
            raise AsmError(f"line {line_no}: expected offset($base), got '{args[1]}'")
        offset = parse_int(m.group(1) or "0", line_no)
        base = reg(m.group(2), line_no)
        if rt == SP:
            raise AsmError(f"line {line_no}: $sp cannot be loaded/stored as data")
        if not 0 <= offset <= 15:
            raise AsmError(f"line {line_no}: memory offset must be 0..15")
        return (op << 12) | (base << 8) | (rt << 4) | offset

    if mnemonic in BRANCH:                       # beq rs, rt, label
        need(3)
        rs, rt = reg(args[0], line_no), reg(args[1], line_no)
        if SP in (rs, rt):
            raise AsmError(f"line {line_no}: $sp cannot be compared")
        target = labels[args[2]] if args[2] in labels else parse_int(args[2], line_no)
        offset = target - (pc + 1)
        if not -8 <= offset <= 7:
            raise AsmError(f"line {line_no}: branch target is {offset} away; "
                           "4-bit offset allows -8..+7 (use a j instead)")
        return (op << 12) | (rs << 8) | (rt << 4) | (offset & 0xF)

    if mnemonic in JUMP:                         # j label
        need(1)
        target = labels[args[0]] if args[0] in labels else parse_int(args[0], line_no)
        if not 0 <= target <= 255:
            raise AsmError(f"line {line_no}: jump target must be 0..255")
        return (op << 12) | (target << 4)

    raise AsmError(f"line {line_no}: cannot encode '{mnemonic}'")


def assemble(source):
    label_idx, program = first_pass(source)
    labels, far = layout(label_idx, program)
    words, listing = [], []
    pc = 0
    for i, (mnemonic, args, line_no, raw) in enumerate(program):
        if i in far:                             # beq x,y,L  ->  bneq x,y,+1 ; j L
            inverse = "bneq" if mnemonic == "beq" else "beq"
            parts = [(inverse, [args[0], args[1], str(pc + 2)]), ("j", [args[2]])]
        else:
            parts = [(mnemonic, args)]
        for m, a in parts:
            word = encode(m, a, pc, labels, line_no)
            words.append(word)
            text = f"{m} {', '.join(a)}".strip()
            if i in far:
                text += f"   (far {mnemonic} {args[2]})"
            listing.append(f"{pc:02X}  {word:04X}  {word >> 12:04b} {(word >> 8) & 15:04b} "
                           f"{(word >> 4) & 15:04b} {word & 15:04b}   {text}")
            pc += 1
    if len(words) > 256:
        raise AsmError("program is longer than 256 instructions (8-bit PC)")
    return words, listing


def to_logisim_image(words):
    body = []
    for i in range(0, len(words), 8):
        body.append(" ".join(f"{w:04x}" for w in words[i:i + 8]))
    return "v2.0 raw\n" + "\n".join(body) + "\n"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src_path = sys.argv[1]
    out_path = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else \
        re.sub(r"\.\w+$", "", src_path) + ".hex"
    with open(src_path) as f:
        source = f.read()
    try:
        words, listing = assemble(source)
    except AsmError as e:
        print("Error:", e)
        sys.exit(2)
    with open(out_path, "w") as f:
        f.write(to_logisim_image(words))
    print("PC  WORD  opcd  f1   f2   f3     source")
    print("\n".join(listing))
    print(f"\n{len(words)} instruction(s) written to {out_path}")


if __name__ == "__main__":
    main()
