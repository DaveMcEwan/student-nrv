# Identifying the most common sequences where registers are read from 
#   (rs) or written to (rd)

# Input : Trimmed down instruction trace
# Output : TODO

# Example to guide use:
# Run the command : python3 scripts/reg_patterns/reg_only_pairs.py < scripts/example.trc
#   while in the base directory

import sys
import csv
import argparse
import os

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # ISA argument stored in args.isa

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common.isa_management import check_isa
from common.reg_functions import parse_instruction

# Helper function that checks if an item is in the input dictionary and increments
#   if it is or creates a key if it doesn't exist
def append_to_counter_dict(dict, insn_name):
    if(insn_name in dict):
        dict[insn_name] += 1
    else:
        dict[insn_name] = 1

# Iterate through instruction trace and count the most frequent register access pairs
def track_rs_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    # String variable forming the base which we'll make the keys from
    key_string = ""

    for line in instr_trace:
        rs1, rs2, _ = parse_instruction(line.split()[2:], all_instrs)
        # print("rs1 :"+rs1+", rs2:"+rs2)

        if rs1: # Variable present in rs1, append to pairing
            if key_string: # If the pair string already has a reg in it
                key_string += rs1
                # print("Adding single: "+rs1)
                append_to_counter_dict(pairs_dict, key_string)
                # print("Adding: "+key_string)
                key_string = ""
            else: # key_string is empty
                # print("Starting with: "+rs1)
                key_string += rs1 + ", "
            if rs2: # Check if rs2 is present (only if rs1 is present)
                if key_string:
                    key_string += rs2
                    # print("Adding single: "+rs2)
                    append_to_counter_dict(pairs_dict, key_string)
                    # print("Adding: "+key_string)
                    key_string = ""
                else:
                    key_string += rs2 + ", "
                    # print("Starting with: "+rs2)
    
    # Sort based on the corresponding counter values
    sorted_pairs = sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_pairs

def track_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    # String variable forming the base which we'll make the keys from
    key_string = ""

    for line in instr_trace:
        _, _, rd = parse_instruction(line.split()[2:], all_instrs)
        # print(rd)
        if rd:
            if key_string:
                key_string += rd
                append_to_counter_dict(pairs_dict, key_string)
                key_string = ""
            else:
                key_string += rd + ", "

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

def track_rs_rd_pairs(instr_trace, all_instrs):
    rs_dict = {}
    rd_dict = {}
    # String variable forming the base which we'll make the keys from
    rs_string = ""
    rd_string = ""

    for line in instr_trace:
        rs1, rs2, rd = parse_instruction(line.split()[2:], all_instrs)
        # print("rs1 :"+rs1+", rs2:"+rs2+", rd:"+rd)
        if rs1:
            if rs_string:
                rs_string += rs1
                append_to_counter_dict(rs_dict, rs_string)
                rs_string = ""
            else:
                rs_string += rs1 + ", "
            if rs2:
                if rs_string:
                    rs_string += rs2
                    append_to_counter_dict(rs_dict, rs_string)
                    rs_string = ""
                else:
                    rs_string += rs2 + ", "
        if rd:
            if rd_string:
                rd_string += rd
                append_to_counter_dict(rd_dict, rd_string)
                rd_string = ""
            else:
                rd_string += rd + ", "

    sorted_rs = sorted(rs_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_rd = sorted(rd_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_rs, sorted_rd

# Takes in the list of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    print("Printing pairs")
    for pair in sorted_pairs:
        print(f'{f"{pair[0]}":<32} {str(pair[1])}')

def main():
    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    # print("Most common RS pairs")
    # print_pairs(track_rs_pairs(instr_trace, all_instrs))
    # print("Most common RD pairs")
    # print_pairs(track_rd_pairs(instr_trace, all_instrs))

    rs_list, rd_list = track_rs_rd_pairs(instr_trace, all_instrs)
    print("Most common RS pairs")
    print_pairs(rs_list)
    print("Most common RD pairs")
    print_pairs(rd_list)

if __name__ == "__main__":
    main()