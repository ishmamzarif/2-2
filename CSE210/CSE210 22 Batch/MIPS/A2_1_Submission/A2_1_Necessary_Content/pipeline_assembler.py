import re

# -------------------------------------------------
# 1. Instruction → Letter mapping  [IMMUTABLE]
# -------------------------------------------------
INSTRUCTION_LETTER = {
    "add":  "A", "addi": "B", "sub":  "C", "subi": "D",
    "and":  "E", "andi": "F", "or":   "G", "ori":  "H",
    "sll":  "I", "srl":  "J", "nor":  "K", "lw":   "L",
    "sw":   "M", "beq":  "N", "bneq": "O", "j":    "P"
}

# -------------------------------------------------
# 2. Instruction ordering  [IMMUTABLE]
# -------------------------------------------------
ORDERING = "CIMBLEHDAGOJPKFN"
OPCODE = {letter: i for i, letter in enumerate(ORDERING)}

# -------------------------------------------------
# 3. Register map  [IMMUTABLE]
# -------------------------------------------------
REGISTER_MAP = {
    "$zero": 0, "$t0": 1, "$t1": 2, "$t2": 3, "$t3": 4, "$t4": 5, "$sp": 6,
}

def reg_number(reg):
    if reg not in REGISTER_MAP:
        raise ValueError(f"Invalid register used: {reg}")
    return REGISTER_MAP[reg]

def to_hex4(value):
    return f"{value & 0xFFFF:04X}"

def to_hex3(value):
    return f"{value & 0xFFF:03X}"

# -------------------------------------------------
# 4. ALU operation codes (3-bit) [IMMUTABLE]
# -------------------------------------------------
ALU_OP = {
    "add":0, "addi":0, "lw":0, "sw":0,
    "sub":1, "subi":1, "beq":1, "bneq":1,
    "and":2, "andi":2, "or":3, "ori":3,
    "nor":4, "sll":5, "srl":6, "j":0
}

# -------------------------------------------------
# 5. Control signal generator (12-bit) [IMMUTABLE]
# -------------------------------------------------
def control_signals(mnemonic):
    regdst = alusrc = memtoreg = regwrite = 0
    memread = memwrite = beq = bneq = jump = 0

    if mnemonic in ["add","sub","and","or","nor"]:
        regdst = 1
        regwrite = 1
    elif mnemonic in ["sll", "srl", "addi","subi","andi","ori"]:
        alusrc = 1
        regwrite = 1
    elif mnemonic == "lw":
        alusrc = 1
        memtoreg = 1
        regwrite = 1
        memread = 1
    elif mnemonic == "sw":
        alusrc = 1
        memwrite = 1
    elif mnemonic == "beq":
        beq = 1
    elif mnemonic == "bneq":
        bneq = 1
    elif mnemonic == "j":
        jump = 1

    aluop = ALU_OP[mnemonic]

    value = (
        (regdst   << 11) | (alusrc   << 10) | (memtoreg << 9) |
        (regwrite <<  8) | (memread  <<  7) | (memwrite << 6) |
        (beq      <<  5) | (bneq    <<  4)  | (jump     << 3) | aluop
    )
    return value

# -------------------------------------------------
# 6. Instruction info extractor
# -------------------------------------------------
def get_info(inst_str):
    """
    Returns a dict with:
      type : "NOP" | "R" | "S" | "I" | "M" | "B" | "J"
      dst  : destination register (or None)
      src  : list of source registers
      m    : mnemonic (or None for NOP)
    """
    if inst_str == "NOP":
        return {"type": "NOP", "dst": None, "src": [], "m": None}
    p = re.split(r"[,\s()]+", inst_str)
    # filter empty strings that can appear after split
    p = [x for x in p if x]
    m = p[0]
    if m in ["add", "sub", "and", "or", "nor"]:
        return {"type": "R", "dst": p[1], "src": [p[2], p[3]], "m": m}
    if m in ["sll", "srl"]:
        return {"type": "S", "dst": p[1], "src": [p[2]], "m": m}
    if m in ["addi", "subi", "andi", "ori"]:
        return {"type": "I", "dst": p[1], "src": [p[2]], "m": m}
    if m == "lw":
        # lw $dst, offset($base)  → parts: [lw, dst, offset, base]
        return {"type": "LW", "dst": p[1], "src": [p[3]], "m": m}
    if m == "sw":
        # sw $src, offset($base)  → parts: [sw, src, offset, base]
        return {"type": "SW", "dst": None, "src": [p[1], p[3]], "m": m}
    if m in ["beq", "bneq"]:
        return {"type": "B", "dst": None, "src": [p[1], p[2]], "m": m}
    if m == "j":
        return {"type": "J", "dst": None, "src": [], "m": m}
    return None

# -------------------------------------------------
# 7. NOP count calculator
#
# Pipeline: IF → ID → EX → MEM → WB  (5 stages, no forwarding)
#
# The rule: the producing instruction writes its result in WB.
# The consuming instruction reads its operands in ID.
#
# If producer is at distance d instructions before consumer
# (d=1 → immediately before, d=2 → two back, etc.) and we
# insert N NOPs between them, the effective distance becomes d + N.
#
# For a register result to be available in ID of the consumer,
# WB of the producer must have completed before ID of the consumer.
# With d=1 (adjacent), we need N=2 NOPs for R/I/S-type producers.
# For lw (load-use): the value isn't available until end of MEM,
# which is one stage later → N=2 for lw at distance 1 as well
# (same cycle count, load-use still needs 2 NOPs without forwarding).
# For sw → lw (memory hazard): the store writes memory in MEM;
# the subsequent load reads memory also in MEM.  The load's MEM
# must come AFTER the store's MEM, so we need one extra bubble →
# N=3 NOPs between sw and lw.
#
# General formula (no forwarding):
#   nops = max(0, STALLS_NEEDED[producer_type] - (d - 1))
# where d is the "raw" distance before any NOPs are inserted,
# and STALLS_NEEDED is the base number of NOPs required when d=1.
#
# STALLS_NEEDED per producer type when distance = 1:
#   R / I / S     → 2
#   LW (load-use) → 2  (same as above; forwarding would make it 1)
#   SW → LW mem   → 3  (handled as a special case below)
# -------------------------------------------------
STALLS_AT_DIST1 = {
    "R":  2,
    "I":  2,
    "S":  2,
    "LW": 2,
    "SW": 0,   # sw has no dst register; memory hazard handled separately
    "B":  0,
    "J":  0,
    "NOP": 0,
}

def nops_for_pair(producer, distance):
    """
    Returns how many NOPs are still needed between `producer`
    (already in final_program at `distance` slots back) and the
    current consumer, given that `distance` real instructions
    already separate them.

    distance=1 → producer is immediately before consumer (no gap).
    """
    ptype = producer["type"]
    base_stalls = STALLS_AT_DIST1.get(ptype, 0)
    needed = max(0, base_stalls - (distance - 1))
    return needed


def nops_for_sw_lw(sw_distance):
    """
    Special case: sw followed eventually by lw to same/overlapping
    address.  sw writes memory in MEM; lw reads memory in MEM.
    We need lw's MEM to be strictly after sw's MEM → 3 NOPs at dist=1.
    """
    base_stalls = 3
    return max(0, base_stalls - (sw_distance - 1))


# -------------------------------------------------
# 8. Pipeline Assembler with Hazard Stalling
# -------------------------------------------------
def assemble_pipelined(program_text):
    # --- Clean lines ---
    lines = [l.split("#")[0].strip() for l in program_text.splitlines() if l.split("#")[0].strip()]

    raw_instructions = []
    initial_labels = {}
    temp_idx = 0
    for line in lines:
        if line.endswith(":"):
            initial_labels[line[:-1]] = temp_idx
        else:
            raw_instructions.append(line)
            temp_idx += 1

    # --- Pass 2: Insert NOPs ---
    final_program = []   # list of instruction strings (including NOPs)
    old_to_new_pc = {}
    current_new_pc = 0

    for i, inst_str in enumerate(raw_instructions):
        old_to_new_pc[i] = current_new_pc
        curr = get_info(inst_str)

        # -------------------------------------------------------
        # Hazard detection: examine the last 3 *real* instructions
        # in final_program (skip NOPs when counting distance).
        # -------------------------------------------------------
        nops_needed = 0

        if curr["src"]:   # consumer has source registers to check
            real_dist = 0  # counts only non-NOP slots
            for slot in reversed(final_program):
                if slot == "NOP":
                    continue          # NOPs don't count as real distance
                real_dist += 1
                if real_dist > 3:
                    break             # beyond pipeline hazard window

                producer = get_info(slot)
                if producer is None:
                    continue

                # --- Register RAW hazard ---
                if (producer["dst"]
                        and producer["dst"] != "$zero"
                        and producer["dst"] in curr["src"]):
                    n = nops_for_pair(producer, real_dist)
                    nops_needed = max(nops_needed, n)

                # --- Memory hazard: sw → lw on same/any address ---
                # (conservative: we don't track addresses at compile time,
                #  so flag any sw before a lw within the hazard window)
                if producer["type"] == "SW" and curr["type"] == "LW":
                    n = nops_for_sw_lw(real_dist)
                    nops_needed = max(nops_needed, n)

        # Insert the computed number of NOPs before current instruction
        for _ in range(nops_needed):
            final_program.append("NOP")
            current_new_pc += 1

        # Re-map current instruction's new PC after any inserted NOPs
        old_to_new_pc[i] = current_new_pc

        # Append current instruction
        final_program.append(inst_str)
        current_new_pc += 1

        # Control Hazard: always stall after branch / jump
        if curr["type"] in ["J", "B"]:
            final_program.append("NOP")
            current_new_pc += 1

    # Update labels to their new PC positions
    final_labels = {name: old_to_new_pc[idx] for name, idx in initial_labels.items()}

    # --- Pass 3: Final Hex Encoding ---
    output_hex = []
    for pc, line in enumerate(final_program):
        if line == "NOP":
            output_hex.append("1000")
            continue

        parts = re.split(r"[,\s()]+", line)
        parts = [x for x in parts if x]
        mnemonic = parts[0]
        op = OPCODE[INSTRUCTION_LETTER[mnemonic]] & 0xF

        if mnemonic in ["add", "sub", "and", "or", "nor"]:
            val = (op<<12)|(reg_number(parts[2])<<8)|(reg_number(parts[3])<<4)|reg_number(parts[1])
        elif mnemonic in ["sll", "srl"]:
            val = (op<<12)|(reg_number(parts[2])<<8)|(reg_number(parts[1])<<4)|(int(parts[3])&0xF)
        elif mnemonic in ["addi", "subi", "andi", "ori"]:
            val = (op<<12)|(reg_number(parts[2])<<8)|(reg_number(parts[1])<<4)|(int(parts[3])&0xF)
        elif mnemonic in ["lw", "sw"]:
            val = (op<<12)|(reg_number(parts[3])<<8)|(reg_number(parts[1])<<4)|(int(parts[2])&0xF)
        elif mnemonic in ["beq", "bneq"]:
            offset = (final_labels[parts[3]] - (pc + 1)) & 0xF
            val = (op<<12)|(reg_number(parts[1])<<8)|(reg_number(parts[2])<<4)|offset
        elif mnemonic == "j":
            addr = final_labels[parts[1]] & 0xFF
            val = (op<<12)|(addr<<4)
        else:
            val = 0

        output_hex.append(to_hex4(val))

    return output_hex, final_program   # also return annotated program for debugging


# -------------------------------------------------
# 9. Run Examples
# -------------------------------------------------
LETTER_TO_MNEMONIC = {v: k for k, v in INSTRUCTION_LETTER.items()}
print("=== Control Signals (12-bit hex) ===")
print(" ".join(to_hex3(control_signals(LETTER_TO_MNEMONIC[l])) for l in ORDERING))


instruction = """
# --- 1. DATA HAZARD (RAW) ---
addi $t0, $zero, 3       # t0 = 3
add  $t1, $t0, $t0       # t1 = t0 + t0 = 6

# --- 2. DATA HAZARD (Load-Use) ---
lw   $t1, 0($t0)         # t2 = mem[t0] = 6
sub  $t3, $t2, $t0       # t3 = t2 - t0 = 0 - 3 = 13 = d

# --- 3. CONTROL HAZARD (Branch) ---
beq  $t3, $t1, target    # if (t3 == t1) → jump (3 != 6 → no jump)
subi $t0, $t0, 1         # t0 = t0 - 1 = 2

target:
# --- 4. STRUCTURAL HAZARD ---
sw   $t3, 4($t1)         # mem[t1 + 4] = t3 → mem[6 + 4] = mem[10] = 3
and  $t4, $t0, $t1       # t4 = t0 & t1 = 2 & 6 = 2

# --- 5. CONTROL HAZARD (Jump) ---
j    end                 # jump to end
ori  $t0, $zero, 5       # (skipped due to jump)

end:
nor  $t4, $t1, $zero     # t4 = ~(t1 | 0) = ~6 = -7
"""

print("\n=== hazard test) ===")
machine_results, annotated = assemble_pipelined(instruction)
print("Annotated program with NOPs:")
for idx, inst in enumerate(annotated):
    print(f"  [{idx:02d}] {inst}")
print("\nMachine code:", " ".join(machine_results))

with open("pipeline_program.hex", "w") as f:
    f.write("v2.0 raw\n")
    for instr in machine_results:
        f.write(instr + "\n")
