# ----------------- Assembly to 20-bit Hex Converter -----------------

import sys

OPCODES = {
    "NOP": "00000", "ADD": "00100", "SUB": "00101", "MUL": "00110",
    "AND": "01000", "OR":  "01001", "XOR": "01010", "NOT": "01011",
    "BC":  "10000", "BZ":  "10001", "BNZ": "10010", "BNG": "10011",
    "B":   "10100", "PSH": "10110", "POP": "10111", "RD":  "11000",
    "WR":  "11001", "LD":  "11100", "ST":  "11101", "MOV": "11110"
}



def reg_3b(reg: str) -> str:
    """Convert rX to 3-bit binary (r0–r7)."""
    return format(int(reg.replace("r", "")), "03b")



def imm_8b(value: int) -> str:
    """Convert immediate number to 8-bit binary."""
    return format(value & 0xFF, "08b")



def assemble_binary(line: str) -> str | None:
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
    if instr == "NOP":
        return "00000000000000000000"
    elif instr == "PSH" or instr == "WR":
        # -- We found instruction that require only ----------
        # -- a register                             ----------
        imm_flag = "0"
        r_dest = "000"
        r_src1 = "000"
        imm_or_r_src2 = f"00000{reg_3b(operands[0])}"
    elif instr == "BC" or instr == "BZ" or instr == "BNZ" or \
        instr == "BNG" or instr == "B":
        # -- We found instruction that require only ----------
        # --  a register or an immediate            ----------
        imm_flag = "1"
        r_dest = "000"
        r_src1 = "000"
        temp = 0
        if operands[0].startswith('#'):
            temp = int(operands[0][1:])
        imm_or_r_src2 = imm_8b(temp)
    elif instr == "NOT":
        # -- We found NOT ------------------------------------
        r_dest = reg_3b(operands[0])
        r_src1 = "000"
        imm_or_r_src2 = "00000" + reg_3b(operands[1])
    elif instr == "ST":
        r_src1 = reg_3b(operands[0])
        op2 = operands[1]
        if op2.startswith("#"):
            imm_flag = "1"
            imm_or_r_src2 = imm_8b(int(op2[1:]))
        else:
            imm_flag = "0"
    elif instr == "RD" or instr == "POP":
        r_dest = reg_3b(operands[0])
        imm_flag = "0"
        r_src1 = "000"
        imm_or_r_src2 = "00000000"
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
        return None
    # ------------------------------------------------------------

    return f"{opcode}{imm_flag}{r_dest}{r_src1}{imm_or_r_src2}"



def binary_to_hex(bin_str: str | None) -> str | None:
    """Convert binary string to hex (uppercase, no prefix)."""
    # -- Check if we need to convert to Hex or not ---------------
    if not bin_str:
        # -- If it is a empty line ---------------------------
        return None
    # ------------------------------------------------------------
    val = int(bin_str, 2)
    hex_str = format(val, "05X")
    return hex_str



def cli_args_collect() -> list[str]:
    cli_args = sys.argv
    if len(cli_args) == 1:
        print("Please at least insert a file to convert")
        sys.exit(1)
    elif 2 <= len(cli_args) <= 3:
        input_file = cli_args[1]
        try:
            input_file_part = input_file.split('.')
            try:
                if input_file_part[1] != "ass":
                    print("We need .ass file extension to convert.")
                    sys.exit(1)
            except IndexError:
                print("We need .ass file extension to convert.")
                sys.exit(1)
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
            hex_val = binary_to_hex(assemble_binary(line))
            if hex_val == None:
                continue
            fout.write(hex_val + "\n")

    print(f"Conversion complete. Hex output saved to '{output_file}'.")



if __name__ == "__main__":
    main()
