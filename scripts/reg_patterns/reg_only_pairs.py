# Identifying the most common sequences (in the form of pairs) where 
#   registers are read from (rs) or written to (rd)

# Input : Trimmed down instruction trace
# Output : TODO

# Example to guide use:
# Run the command : python3 scripts/reg_patterns/reg_only_pairs.py < scripts/example.trc
#   while in the base directory

import sys
import csv
import argparse

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # ISA argument stored in args.isa

# https://www.geeksforgeeks.org/python-import-from-parent-directory/
# Path adjusting to be able to append helper functions from scripts/
import os
from tabnanny import check
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import helper as hlp

# Function to take in a CSV file and convert it into the desired dictionary format
def convert_isa(isa_part):
    test_dict = {}
    with open("isa/"+isa_part+".isa", 'r') as data_file:
        data = csv.DictReader(filter(lambda row: row[0]!='#', data_file), skipinitialspace=True, delimiter=',')
        for row in data:
            # Initialise subdirectory
            sub_dict = test_dict.get(row["Insn"], dict())
            # Also want to include information on the instruction type
            #   to understand what the immediate is actually being used for
            sub_dict["Type"] = row["Type"]
            sub_dict["Format"] = row["Format"]

            test_dict[row["Insn"]] = sub_dict

    return test_dict

# Take in the input string detailing the ISA, parse it and grab the needed dictionaries
def check_isa(isa):
    all_instrs = {}

    # Determine base instruction set based on the XLEN
    if int(isa[2:4]) == 32:
        all_instrs.update(convert_isa("rv32"))
    else:
        # No file yet made for this condition
        all_instrs.update(convert_isa("rv64"))
    
    # Include relevant instructions based on the remaining instructions
    for index in range(5, len(isa)):
        all_instrs.update(convert_isa(isa[index]))
    # TODO : Consider extensions such as the bit manip ones which won't be 
    #   represented by just single characters; also need to consider
    #   CSV files which are combinations of extensions

    return all_instrs

# Iterate through instruction trace and count the most frequent register access pairs
# Register access type is determined by the string r_type
def track_rs_pairs(instr_trace, r_type, all_instrs):
    pairs_dict = {}

    rs1, rs2, _ = hlp.parse_instruction(instr_trace[0].split()[2:], all_instrs)

    for line in instr_trace[1:]:
        rs1, rs2, _ = hlp.parse_instruction(line.split()[2:], all_instrs)
        if rs1:
            pass
        if rs2:
            pass


def main():
    
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()

if __name__ == "__main__":
    main()