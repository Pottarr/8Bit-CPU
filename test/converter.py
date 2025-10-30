# ---------- Code Format -----------
# LD    =>  0000   load to register
# MOV   =>  0001   move value
# ST    =>  0010   store data
# RD    =>  0011   read data


# ADD   =>  0100   add 2 data
# SUB   =>  0101   subtract 2 data
# MUL   =>  0110   multiply 2 data


# WR    =>  0111   write register to output


# AND   =>  1000   and 2 data
# OR    =>  1001   or 2 data
# XOR   =>  1010   xor 2 data
# NOT   =>  1011   not a single data

# BC    =>  1100   branch if carry out
# BZ    =>  1101   branch if zero
# BNZ   =>  1110   branch if not zero
# B     =>  1111   unconditional branch

# -------------- Rule --------------
# 19 bits instruction
# bit 1     : immediate mode    true / flase
# bit 2-5   : register destination
# bit 6-8   : register operand 1
# bit 9-11  : register operand 2 (ignore if not used)
# bit 12-19 : 8 bits of binary, last 3 bit are register number for none immediate mode

# ---------- Assembly to 19-bit Binary Converter (File Version) ----------

# ---------- Assembly to 19-bit Hex Converter ----------

import sys

OPCODES = {
    "LD":  "0000",
    "MOV": "0001",
    "ST":  "0010",
    "RD":  "0011",
    "ADD": "0100",
    "SUB": "0101",
    "MUL": "0110",
    "WR":  "0111",
    "AND": "1000",
    "OR":  "1001",
    "XOR": "1010",
    "NOT": "1011",
    "BC":  "1100",
    "BZ":  "1101",
    "BNZ": "1110",
    "B":   "1111"
}

def reg3(reg: str) -> str:
    """Convert rX to 3-bit binary (r0–r7)."""
    return format(int(reg.replace("r", "")), "03b")

def imm8(value: int) -> str:
    """Convert immediate number to 8-bit binary."""
    return format(value & 0xFF, "08b")

def assemble_binary(line: str) -> str:
    """Convert assembly line to 19-bit binary string."""
    line = line.strip()
    if not line or line.startswith("#"):
        return ""
    parts = line.replace(",", "").split()
    instr = parts[0].upper()
    opcode = OPCODES.get(instr, "????")

    flag = "0"
    rd = "000"
    r1 = "000"
    imm_or_reg = "00000000"
    operands = parts[1:]

    def get_operand_bits(op):
        nonlocal flag
        if op.startswith("#"):
            flag = "1"
            return imm8(int(op[1:]))
        else:
            return "00000" + reg3(op)

    if instr == "NOT":
        rd = reg3(operands[0])
        r1 = "000"
        imm_or_reg = "00000" + reg3(operands[1])
    elif len(operands) == 2:
        rd = reg3(operands[0])
        op2 = operands[1]
        if op2.startswith("#"):
            flag = "1"
            imm_or_reg = imm8(int(op2[1:]))
        else:
            flag = "0"
            imm_or_reg = "00000" + reg3(op2)
    elif len(operands) == 3:
        rd = reg3(operands[0])
        r1 = reg3(operands[1])
        imm_or_reg = get_operand_bits(operands[2])
    else:
        return ""

    return f"{flag}{opcode}{rd}{r1}{imm_or_reg}"

def binary_to_hex(bin_str: str) -> str:
    """Convert binary string to hex (uppercase, no prefix)."""
    if not bin_str:
        return ""
    val = int(bin_str, 2)
    hex_str = format(val, "05X")  # 19 bits fit in 5 hex digits (max 0x7FFFF)
    return hex_str

def main():
    input_file = sys.argv[1]
    try:
        output_file = sys.argv[2]
    except IndexError: 
        output_file = f"{input_file.split(".")[0]}.hex"

    with open(input_file, "r") as fin, open(output_file, "w") as fout:
        fout.write("v2.0 raw\n")
        for line in fin:
            binary = assemble_binary(line)
            if binary:
                hex_val = binary_to_hex(binary)
                fout.write(hex_val + "\n")

    print(f"✅ Conversion complete. Hex output saved to '{output_file}'.")

if __name__ == "__main__":
    main()


# assembly_lines = [
#     "MOV r0, #17",      # 1 0001 000 000 00010001
#     "MOV r1, #47",      # 1 0001 001 000 00101111
#     "ADD r2, r1, r0",   # 0 0100 010 001 00000000
#     "SUB r3, r1, r0",   # 0 0101 011 001 00000000
#     "LD  r1, r3",       # 0 0000 001 000 00000011
#     "MUL r4, r1, #5",   # 1 0110 100 001 00000101
#     "NOT r5, r4",       # 0 1011 101 000 00000100
#     "AND r6, r5, r4",   # 0 1000 110 101 00000 100
#     "SUB r4, r4, #1",   # 1 0101 100 100 00000001
#     "BZ r4, #9"         # 1 1101 100 000 00001001
# ]

