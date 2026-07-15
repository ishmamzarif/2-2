import re
import os

# -------------------------------------------------
# 1. Instruction → Letter mapping  [IMMUTABLE]
# -------------------------------------------------
INSTRUCTION_LETTER = {
    "add":  "A",
    "addi": "B",
    "sub":  "C",
    "subi": "D",
    "and":  "E",
    "andi": "F",
    "or":   "G",
    "ori":  "H",
    "sll":  "I",
    "srl":  "J",
    "nor":  "K",
    "lw":   "L",
    "sw":   "M",
    "beq":  "N",
    "bneq": "O",
    "j":    "P"
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
    "$zero": 0,
    "$t0":   1,
    "$t1":   2,
    "$t2":   3,
    "$t3":   4,
    "$t4":   5,
    "$sp":   6,
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
# 4. ALU operation codes (3-bit)
# -------------------------------------------------
ALU_OP = {
    "add":0, "addi":0, "lw":0, "sw":0,
    "sub":1, "subi":1, "beq":1, "bneq":1,
    "and":2, "andi":2,
    "or":3,  "ori":3,
    "nor":4,
    "sll":5,
    "srl":6,
    "j":0
}

# -------------------------------------------------
# 5. Control signal generator (12-bit)
# -------------------------------------------------
def control_signals(mnemonic):

    regdst = alusrc = memtoreg = regwrite = 0
    memread = memwrite = beq = bneq = jump = 0

    if mnemonic in ["add","sub","and","or","nor"]:
        regdst = 1
        regwrite = 1
    
    elif mnemonic in ["sll", "srl"]:
        alusrc = 1
        regwrite = 1
    
    elif mnemonic in ["addi","subi","andi","ori"]:
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
        (regdst  << 11) |
        (alusrc  << 10) |
        (memtoreg<< 9 ) |
        (regwrite<< 8 ) |
        (memread << 7 ) |
        (memwrite<< 6 ) |
        (beq     << 5 ) |
        (bneq    << 4 ) |
        (jump    << 3 ) |
        aluop
    )

    return value

# -------------------------------------------------
# 6. Assembler (STRICT ISA FORMATS)
# -------------------------------------------------
def assemble(program_text):

    lines = program_text.splitlines()

    # remove comments/blank lines
    clean = []
    for line in lines:
        line = line.split("#")[0].strip()
        if line:
            clean.append(line)

    # -------------------------------------------------
    # Macro expansion: push/pop → real instructions
    #   push $rt  →  subi $sp, $sp, 1
    #                sw $rt, 0($sp)
    #
    #   pop $rt   →  lw $rt, 0($sp)
    #                addi $sp, $sp, 1
    # -------------------------------------------------
    expanded = []
    for line in clean:
        if line.endswith(":"):
            # labels pass through unchanged
            expanded.append(line)
            continue

        parts_check = re.split(r"[,\s()]+", line)
        parts_check = [p for p in parts_check if p]
        if not parts_check:
            continue

        mnemonic_check = parts_check[0]

        if mnemonic_check == "push":
            rt = parts_check[1]
            expanded.append(f"subi $sp, $sp, 1")
            expanded.append(f"sw {rt}, 0($sp)")

        elif mnemonic_check == "pop":
            rt = parts_check[1]
            expanded.append(f"lw {rt}, 0($sp)")
            expanded.append(f"addi $sp, $sp, 1")

        else:
            expanded.append(line)

    clean = expanded

    # pass 1: collect labels
    labels = {}
    instructions = []
    pc = 0

    for line in clean:
        if line.endswith(":"):
            labels[line[:-1]] = pc
        else:
            instructions.append(line)
            pc += 1

    # pass 2: encode
    output = []
    pc = 0

    for line in instructions:
        parts = re.split(r"[,\s()]+", line)
        parts = [p for p in parts if p]

        mnemonic = parts[0]
        opcode = OPCODE[INSTRUCTION_LETTER[mnemonic]] & 0xF

        # ---------------- R-TYPE ----------------
        if mnemonic in ["add","sub","and","or","nor"]:
            rd = reg_number(parts[1])
            rs = reg_number(parts[2])
            rt = reg_number(parts[3])
            value = (opcode<<12)|(rs<<8)|(rt<<4)|rd

        # ---------------- S-TYPE ----------------
        elif mnemonic in ["sll","srl"]:
            rd = reg_number(parts[1])
            rt = reg_number(parts[2])   # source register
            shamt = int(parts[3]) & 0xF
            value = (opcode<<12)|(rt<<8)|(rd<<4)|shamt

        # ---------------- I-TYPE ALU ------------
        elif mnemonic in ["addi","subi","andi","ori"]:
            rt = reg_number(parts[1])
            rs = reg_number(parts[2])
            imm = int(parts[3]) & 0xF
            value = (opcode<<12)|(rs<<8)|(rt<<4)|imm

        # ---------------- I-TYPE MEMORY ---------
        elif mnemonic in ["lw","sw"]:
            rt = reg_number(parts[1])
            imm = int(parts[2]) & 0xF
            rs = reg_number(parts[3])
            value = (opcode<<12)|(rs<<8)|(rt<<4)|imm

        # ---------------- I-TYPE BRANCH ---------
        elif mnemonic in ["beq","bneq"]:
            rs = reg_number(parts[1])
            rt = reg_number(parts[2])
            label = parts[3]
            offset = labels[label] - (pc + 1)

            if not (-8 <= offset <= 7):
                raise ValueError(f"Branch offset overflow at PC={pc}")

            value = (opcode<<12)|(rs<<8)|(rt<<4)|(offset & 0xF)

        # ---------------- J-TYPE ----------------
        elif mnemonic == "j":
            label = parts[1]
            address = labels[label] & 0xFF
            value = (opcode<<12)|(address<<4)

        else:
            raise ValueError(f"Unknown instruction: {mnemonic}")

        output.append((mnemonic, to_hex4(value)))
        pc += 1

    return output

# -------------------------------------------------
# 7. Main Execution & File I/O
# -------------------------------------------------
if __name__ == "__main__":
    
    # Changed input file from .asm to .txt
    input_file = "input.txt"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found.")
        print("Please create a file named 'input.txt' in the same folder and add your assembly code to it.")
        exit(1)
        
    # Read assembly code from text file
    with open(input_file, "r") as f:
        program_text = f.read()

    try:
        # Run assembler
        machine_code = assemble(program_text)
        
        # Extract hex codes into a flat list
        hex_codes = [code for _, code in machine_code]
        instructions_string = " ".join(hex_codes)
        
        # ---------------------------------------------
        # Terminal Output
        # ---------------------------------------------
        print("=== Machine Code (16-bit) ===")
        print(instructions_string)
        print(f"\nTotal number of instructions (4-hex-bit sets): {len(hex_codes)}")
        
        LETTER_TO_MNEMONIC = {v:k for k,v in INSTRUCTION_LETTER.items()}
        control_signals_list = [to_hex3(control_signals(LETTER_TO_MNEMONIC[l])) for l in ORDERING]
        controls_string = " ".join(control_signals_list)
        
        print("\n=== Control Signals (12-bit hex) ===")
        print(controls_string)

        # ---------------------------------------------
        # File Outputs
        # ---------------------------------------------
        
        # Write instructions.hex (Only necessary hex, all sequentially)
        with open("instructions.hex", "w") as f:
            f.write("v2.0 raw\n")
            f.write(instructions_string)
            
        # Write rom_controls.hex (Only necessary hex, all sequentially)
        with open("rom_controls.hex", "w") as f:
            f.write("v2.0 raw\n")
            f.write(controls_string)
            
        print("\n[SUCCESS] Saved 'instructions.hex' and 'rom_controls.hex'.")

    except Exception as e:
        print(f"Failed to assemble code. Error: {e}")