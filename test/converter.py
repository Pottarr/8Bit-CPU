# ----------------- Assembly to 19-bit Hex Converter -----------------
# converter.py

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

def reg_3b(reg: str) -> str:
    """Convert rX to 3-bit binary (r0–r7)."""
    return format(int(reg.replace("r", "")), "03b")

def imm_8b(value: int) -> str:
    """Convert immediate number to 8-bit binary."""
    return format(value & 0xFF, "08b")

def assemble_binary(line: str) -> str:
    """Convert assembly line to 19-bit binary string."""
    
    # -- Remove comments while compiling -------------------------
    if ";" in line:
        line = line.split(';')[0]
    # ------------------------------------------------------------

    # -- Decode Opcode to Binary ---------------------------------
    line = line.strip()
    if not line or line.startswith("#"):
        return ""
    parts = line.replace(",", "").split()
    instr = parts[0].upper()
    opcode = OPCODES.get(instr, "????")
    # ------------------------------------------------------------

    # -- Set default binary --------------------------------------
    imm_flag = "0"
    r_dest = "000"
    r_src1 = "000"
    imm_or_r_src2 = "00000000"
    operands = parts[1:]
    # ------------------------------------------------------------

    def get_operand_bits(opnd) -> str:
        """Get operands binary bits"""
        nonlocal imm_flag
        # -- Check if second operand is immediate ------------
        if opnd.startswith("#"):
            # True: Set IsImm flag to 1 ------------------
            imm_flag = "1"
            return imm_8b(int(opnd[1:]))
        else:
            # False: Set IsImm flag to 0 -----------------
            return "00000" + reg_3b(opnd)
        # ----------------------------------------------------

    # Assemble binary for each commnand --------------------------
    if instr == "NOT":
        # -- We found NOT ------------------------------------
        r_dest = reg_3b(operands[0])
        r_src1 = "000"
        imm_or_r_src2 = "00000" + reg_3b(operands[1])
    elif len(operands) == 2:
        # -- We found instruction which need 2 operands ------
        r_dest = reg_3b(operands[0])
        op2 = operands[1]
        if op2.startswith("#"):
            imm_flag = "1"
            imm_or_r_src2 = imm_8b(int(op2[1:]))
        else:
            imm_flag = "0"
            imm_or_r_src2 = "00000" + reg_3b(op2)
    elif len(operands) == 3:
        # -- We found instruction which need 3 operands ------
        r_dest = reg_3b(operands[0])
        r_src1 = reg_3b(operands[1])
        imm_or_r_src2 = get_operand_bits(operands[2])
    else:
        # -- We found empty line -----------------------------
        return ""
    # ------------------------------------------------------------

    return f"{imm_flag}{opcode}{r_dest}{r_src1}{imm_or_r_src2}"

def binary_to_hex(bin_str: str) -> str:
    """Convert binary string to hex (uppercase, no prefix)."""
    # -- Check if we need to convert to Hex or not ---------------
    if not bin_str:
        # -- If it is a empty line ---------------------------
        return ""
    # ------------------------------------------------------------
    val = int(bin_str, 2)
    hex_str = format(val, "05X")  # 19 bits fit in 5 hex digits
                                  # (max 0x7FFFF)
    return hex_str

def cli_args_collect() -> list[str]:
    cli_args = sys.argv
    if len(cli_args) == 1:
        print("Please at least insert a file to convert")
        sys.exit(1)
    elif 2 <= len(cli_args) <= 3:
        input_file = cli_args[1]
        try:
            _ = input_file.split('.')
        except IndexError:
            output_file = f"{input_file}.hex"
        output_file = f"{input_file.split('.')[0]}.hex"

        if len(cli_args) == 3:
            output_file = cli_args[2]
            try:
                _ = output_file.split('.')[1]
            except IndexError:
                output_file = f"{output_file}.hex"
                print("Do not forget to add file extension .hex")
            if output_file.split('.')[1] != "hex":
                output_file = f"{output_file.split('.')[0]}.hex"
                print("Do not forget to change file extension to .hex")
    else:
        print("Too many arguments")
        sys.exit(1)
    return [input_file, output_file]


def main():
    [input_file, output_file] = cli_args_collect()

    with open(input_file, "r") as fin, open(output_file, "w") as fout:
        fout.write("v2.0 raw\n")
        for line in fin:
            binary = assemble_binary(line)
            if binary:
                hex_val = binary_to_hex(binary)
                fout.write(hex_val + "\n")

    print(f"Conversion complete. Hex output saved to '{output_file}'.")

if __name__ == "__main__":
    main()
