import os

# -------------------------------------------------
# Instruction → Letter mapping
# -------------------------------------------------
INSTRUCTION_LETTER = {
    "add":  "A","addi": "B","sub":  "C","subi": "D",
    "and":  "E","andi": "F","or":   "G","ori":  "H",
    "sll":  "I","srl":  "J","nor":  "K","lw":   "L",
    "sw":   "M","beq":  "N","bneq": "O","j":    "P"
}

ORDERING = "CIMBLEHDAGOJPKFN"

# -------------------------------------------------
# ALU operation codes
# -------------------------------------------------
ALU_OP = {
    "add":0,"addi":0,"lw":0,"sw":0,
    "sub":1,"subi":1,"beq":1,"bneq":1,
    "and":2,"andi":2,
    "or":3,"ori":3,
    "nor":4,"sll":5,"srl":6,"j":0
}

# -------------------------------------------------
# Control signal generator (12-bit)
# -------------------------------------------------
def control_signals(mnemonic):
    regdst = alusrc = memtoreg = regwrite = 0
    memread = memwrite = beq = bneq = jump = 0

    if mnemonic in ["add","sub","and","or","nor"]:
        regdst = 1; regwrite = 1
    elif mnemonic in ["sll","srl"]:
        alusrc = 1; regwrite = 1
    elif mnemonic in ["addi","subi","andi","ori"]:
        alusrc = 1; regwrite = 1
    elif mnemonic == "lw":
        alusrc=1; memtoreg=1; regwrite=1; memread=1
    elif mnemonic == "sw":
        alusrc=1; memwrite=1
    elif mnemonic == "beq":
        beq = 1
    elif mnemonic == "bneq":
        bneq = 1
    elif mnemonic == "j":
        jump = 1

    aluop = ALU_OP[mnemonic]

    return (
        (regdst<<11)|(alusrc<<10)|(memtoreg<<9)|(regwrite<<8)|
        (memread<<7)|(memwrite<<6)|(beq<<5)|(bneq<<4)|
        (jump<<3)|aluop
    )

# -------------------------------------------------
# Control signal names
# -------------------------------------------------
CONTROL_NAMES = [
    "RegDst","ALUSrc","MemtoReg","RegWrite",
    "MemRead","MemWrite","Beq","Bneq",
    "Jump","ALUOp2","ALUOp1","ALUOp0"
]

# -------------------------------------------------
# Extract active signals
# -------------------------------------------------
def active_signals(value):
    bits = f"{value:012b}"
    return [CONTROL_NAMES[i] for i, b in enumerate(bits) if b == '1']

# -------------------------------------------------
# Group binary (4-4-4)
# -------------------------------------------------
def grouped_binary(value):
    b = f"{value:012b}"
    return f"{b[0:4]} {b[4:8]} {b[8:12]}"

# -------------------------------------------------
# Hex formatter
# -------------------------------------------------
def to_hex3(value):
    return f"{value & 0xFFF:03X}"

# -------------------------------------------------
# HTML Generator
# -------------------------------------------------
def generate_html():
    LETTER_TO_MNEMONIC = {v:k for k,v in INSTRUCTION_LETTER.items()}
    rows = []

    for letter in ORDERING:
        mnemonic = LETTER_TO_MNEMONIC[letter]
        val = control_signals(mnemonic)

        signals = active_signals(val)
        signal_str = ", ".join(signals) if signals else "—"

        bin_str = grouped_binary(val)
        hex_str = to_hex3(val)

        rows.append(f"""
        <tr>
            <td>{mnemonic}</td>
            <td>{letter}</td>
            <td>{signal_str}</td>
            <td>{bin_str}</td>
            <td>0x{hex_str}</td>
        </tr>
        """)

    # Legend for 12-bit control signals
    bit_positions = "11 10 9 8 7 6 5 4 3 2 1 0"
    signals_legend = "RegDst ALUSrc MemtoReg RegWrite MemRead MemWrite Beq Bneq Jump ALUOp2 ALUOp1 ALUOp0"
    grouped_legend = "[Reg/Mem/Branch/Jump] [ALUOp]"

    html = f"""
    <html>
    <head>
        <title>Control Signals</title>
        <style>
            body {{
                font-family: monospace;
                background: #ffffff;
                color: #000000;
            }}
            table {{
                border-collapse: collapse;
                width: 90%;
                margin: auto;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background: #fafafa;
            }}
            caption {{
                text-align: left;
                margin-top: 10px;
                font-size: 0.95em;
            }}
            .legend {{
                width: 90%;
                margin: auto;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>

    <h2 style="text-align:center;">Control Signals (Active + Encoded)</h2>

    <table>
        <tr>
            <th>Instruction</th>
            <th>Opcode</th>
            <th>Active Signals</th>
            <th>Binary (4-4-4)</th>
            <th>Hex</th>
        </tr>
        {''.join(rows)}
    </table>

    <div class="legend">
        <p><b>Bit Positions:</b> {bit_positions}</p>
        <p><b>Signals:</b> {signals_legend}</p>
        <p><b>Grouping:</b> {grouped_legend}</p>
    </div>

    </body>
    </html>
    """

    with open("control_signals.html", "w") as f:
        f.write(html)

# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    generate_html()
    print("[SUCCESS] control_signals.html generated")