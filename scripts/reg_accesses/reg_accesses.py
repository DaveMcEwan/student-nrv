# Analyse the instruction trace input through stdin
# Measure how frequently specific registers are accessed

# Input : Trimmed down instruction trace
# Output : TODO

# Example to guide use:
# Run the command : python3 scripts/reg_accesses/reg_accesses.py < scripts/example.trc
#   while in the base directory

import sys
import argparse
import csv

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
args = parser.parse_args() # ISA argument stored in args.isa

# Function to take in a CSV file and convert it into the desired dictionary format
def convert_reg_only(isa_part):
    test_dict = {}
    with open("isa/"+isa_part+".isa", 'r') as data_file:
        data = csv.DictReader(filter(lambda row: row[0]!='#', data_file), skipinitialspace=True, delimiter=',')
        for row in data:
            test_dict[row["Insn"]] = int(row["Reg_Type"])

    return test_dict

# Take in the input string detailing the ISA, parse it and grab the needed dictionaries
def check_isa(isa):
    all_instrs = {}

    # Determine base instruction set based on the XLEN
    if int(isa[2:4]) == 32:
        all_instrs.update(convert_reg_only("rv32"))
    else:
        # No file yet made for this condition
        all_instrs.update(convert_reg_only("rv64"))
    
    # Include relevant instructions based on the remaining instructions
    for index in range(5, len(isa)):
        all_instrs.update(convert_reg_only(isa[index]))
    # TODO : Consider extensions such as the bit manip ones which won't be 
    #   represented by just single characters; also need to consider
    #   CSV files which are combinations of extensions

    return all_instrs

# Helper function that checks if an item is in the input dictionary and increments
#   if it is or creates a key if it doesn't exist
def append_to_counter_dict(dict, insn_name):
    if(insn_name in dict):
        dict[insn_name] += 1
    else:
        dict[insn_name] = 1

# Iterate through the instruction trace and measure the frequency at which
#   registers are accessed
def track_regs(instr_trace, all_instrs):
    # Initialise variables and dictionaries
    rs_dict = {}
    rd_dict = {}
    imm_dict = {}

    # TODO : Expand program to look at other categories such as the 'Type' 
    #   and use this to determine what the immediate is for
    offset_dict = {}
    shift_dict = {}

    # Parse lines on stdin
    for line in instr_trace:
        line_list = line.split()
        insn_name = line_list[2]

        # Check for instruction in overall dictionary
        if insn_name in all_instrs:
            # Check what the register operand format is and assign variables accordingly
            if all_instrs[insn_name] == "R":
                # rd, rs1, rs2
                append_to_counter_dict(rd_dict, line_list[3][:-1])
                append_to_counter_dict(rs_dict, line_list[4][:-1])
                append_to_counter_dict(rs_dict, line_list[5])
            elif all_instrs[insn_name] == "I":
                # rd, imm(rs)
                append_to_counter_dict(rd_dict, line_list[3][:-1])
                # Parse the second part of the assembly register format
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                # Not converting immediates to ints as we may get immediates as hex values
                append_to_counter_dict(imm_dict, remaining_string[0])
                append_to_counter_dict(rs_dict, remaining_string[1])
            elif all_instrs[insn_name] == "S":
                # rs1, imm(rs2)
                append_to_counter_dict(rs_dict, line_list[3][:-1])
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                append_to_counter_dict(rs_dict, remaining_string[1])
            elif all_instrs[insn_name] == "U":
                # rd, imm
                append_to_counter_dict(rd_dict, line_list[3][:-1])
                append_to_counter_dict(imm_dict, line_list[4])
            elif all_instrs[insn_name] == "SB":
                # rs1, rs2, pc + imm
                append_to_counter_dict(rs_dict, line_list[3][:-1])
                append_to_counter_dict(rs_dict, line_list[4][:-1])
                append_to_counter_dict(imm_dict, line_list[7])
            elif all_instrs[insn_name] == "UJ":
                # pc + imm
                append_to_counter_dict(rd_dict, "ra") # Return Address register
                append_to_counter_dict(imm_dict, line_list[4]+line_list[5])
            elif all_instrs[insn_name] == "CR":     # Compressed formats
                # rs/d, rs
                first_reg = line_list[3][:-1]
                # Append to both rs and rd dictionaries since the first register
                #   is both read from and written to
                append_to_counter_dict(rs_dict, first_reg)
                append_to_counter_dict(rd_dict, first_reg)
                append_to_counter_dict(rs_dict, line_list[4])
            elif all_instrs[insn_name] == "CI":
                # rs/d, imm,
                first_reg = line_list[3][:-1]
                append_to_counter_dict(rs_dict, first_reg)
                append_to_counter_dict(rd_dict, first_reg)
                append_to_counter_dict(imm_dict, line_list[4])
            elif all_instrs[insn_name] == "CSS":
                # rs, imm(sp)
                append_to_counter_dict(rs_dict, line_list[3][:-1])
                append_to_counter_dict(imm_dict, line_list[4].split("(")[0])
                append_to_counter_dict(rs_dict, "sp")
            elif all_instrs[insn_name] == "CIW":
                # rd, sp, imm
                append_to_counter_dict(rd_dict, line_list[3][:-1])
                append_to_counter_dict(rs_dict, "sp")
                append_to_counter_dict(imm_dict, line_list[5])
            elif all_instrs[insn_name] == "CL":
                # rd, imm(rs) - can merge with  'I'
                append_to_counter_dict(rd_dict, line_list[3][:-1])
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                append_to_counter_dict(rs_dict, remaining_string[1])
            elif all_instrs[insn_name] == "CS":
                # rs1, imm(rs2) - can merge with 'S'
                append_to_counter_dict(rs_dict, line_list[3][:-1])
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                append_to_counter_dict(rs_dict, remaining_string[1])
            elif all_instrs[insn_name] == "CA":
                pass # TODO
            elif all_instrs[insn_name] == "CB":
                # rs, pc + imm
                append_to_counter_dict(rs_dict, line_list[3][:-1])
                append_to_counter_dict(imm_dict, line_list[6])
            elif all_instrs[insn_name] == "CJ":
                # pc + imm
                # TODO : Add specific case for 'jumpl' instruction types where
                #   the return address is added to the rd dictionary
                append_to_counter_dict(rd_dict, "ra") # Return Address register
                append_to_counter_dict(imm_dict, line_list[4]+line_list[5])
            else:
                pass # Do nothing if the column has nothing

def main():
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    track_regs(instr_trace, check_isa(args.isa))

if __name__ == "__main__":
    main()