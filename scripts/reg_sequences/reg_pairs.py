# Identifying the most common sequences (in the form of pairs) where 
#   registers are read from (rs) or written to (rd) individually or both

# Input : Trimmed down instruction trace
# Output : - stdout : Formatted output containing every pair and a counter detailing how
#   often each pair has occurred.
#          - JSON output : Dictionary containing the most common rs and rd pairs to be
#   used in a display script.

# Example to guide use:
# Run the command : python3 scripts/reg_sequences/reg_pairs.py \
#                   --isa=rv32ic
#                   --jsondump=<file to place any json output files>
#  < scripts/example.trc
#   while in the base directory

import sys
import argparse
import os
import json

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--isa", help="RISC-V ISA string")
parser.add_argument("-j", "--jsondump", help="Filepath/name for the JSON files")
args = parser.parse_args() # ISA argument stored in args.isa

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common.isa_management import check_isa
from common.reg_functions import parse_instruction
from common.helper_functions import append_to_counter_dict
from common.pattern_detection import print_pairs

# Iterate through instruction trace and count the most frequent register access pairs (rs)
def track_rs_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    # String variable forming the base which we'll make the keys from
    key_string = ""

    counter = 0
    # Initialise key_string
    while not key_string:
        line = instr_trace[counter]
        rs1, rs2, _ = parse_instruction(line.split()[4:], all_instrs)

        if rs1:
            key_string = rs1 + ", "
            if rs2:
                key_string += rs2
                append_to_counter_dict(pairs_dict, key_string)
                key_string = rs2 + ", "

        counter += 1

    # key_string is guaranteed to have a reg already in it now
    for line in instr_trace[counter:]:
        rs1, rs2, _ = parse_instruction(line.split()[4:], all_instrs)
        # print("rs1 :"+rs1+", rs2:"+rs2)

        if rs1: # Variable present in rs1, append to pairing
            # print("rs1: "+rs1)
            key_string += rs1
            # print("Adding single: "+rs1)
            append_to_counter_dict(pairs_dict, key_string)
            # print("Adding: "+key_string)
            key_string = rs1+ ", "
            if rs2: # Check if rs2 is present (only if rs1 is present)
                # print("rs2: "+rs2)
                key_string += rs2
                # print("Adding single: "+rs2)
                append_to_counter_dict(pairs_dict, key_string)
                # print("Adding: "+key_string)
                key_string = rs2 + ", "
    
    # Sort based on the corresponding counter values
    sorted_pairs = sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_pairs

# Iterate through instruction trace and count the most frequent register access pairs (rd)
def track_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    # String variable forming the base which we'll make the keys from
    key_string = ""

    counter = 0
    # Initialise key_string
    while not key_string:
        line = instr_trace[counter]
        _, _, rd = parse_instruction(line.split()[4:], all_instrs)
        if rd:
            key_string += rd + ", "
        counter += 1

    # key_string is guaranteed to have a reg already in it now
    for line in instr_trace[counter:]:
        _, _, rd = parse_instruction(line.split()[4:], all_instrs)
        if rd:
            # print(rd)
            key_string += rd
            append_to_counter_dict(pairs_dict, key_string)
            key_string = rd+ ", "
    
    # Sort based on the corresponding counter values
    sorted_pairs = sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_pairs

# Function that tracks both rs and rd patterns in a single iteration
def track_rs_rd_pairs(instr_trace, all_instrs):
    rs_dict = {}
    rd_dict = {}
    # String variable forming the base which we'll make the keys from
    rs_string = ""
    rd_string = ""

    counter = 0
    # Initialise strings
    while not rs_string and not rd_string:
        line = instr_trace[counter]
        rs1, rs2, rd = parse_instruction(line.split()[4:], all_instrs)

        if rs1:
            if rs_string: # Already has a reg in it
                rs_string += rs1
                append_to_counter_dict(rs_dict, rs_string)
            rs_string = rs1 + ", "

            if rs2: # Guaranteed to already have a reg in rs_string beforehand
                rs_string += rs2
                append_to_counter_dict(rs_dict, rs_string)
                rs_string = rs2 + ", "

        if rd:
            if rd_string: # Already has a reg
                rd_string += rd
                append_to_counter_dict(rd_dict, rd_string)
            rd_string = rd + ", "
        counter += 1

    for line in instr_trace[counter:]:
        rs1, rs2, rd = parse_instruction(line.split()[4:], all_instrs)
        # print("rs1 :"+rs1+", rs2:"+rs2+", rd:"+rd)

        if rs1:
            # print("rs1: "+rs1)
            rs_string += rs1
            append_to_counter_dict(rs_dict, rs_string)
            rs_string = rs1 + ", "
            if rs2:
                # print("rs2: "+rs2)
                rs_string += rs2
                append_to_counter_dict(rs_dict, rs_string)
                rs_string = rs2 + ", "

        if rd:
            # print("rd: "+rd)
            rd_string += rd
            append_to_counter_dict(rd_dict, rd_string)
            rd_string = rd + ", "

    sorted_rs = sorted(rs_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_rd = sorted(rd_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_rs, sorted_rd

def main():
    all_instrs = check_isa(args.isa)

    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()

    # # Individual pair tracking
    # print("Most common RS pairs")
    # print_pairs(track_rs_pairs(instr_trace, all_instrs))
    # print("Most common RD pairs")
    # print_pairs(track_rd_pairs(instr_trace, all_instrs))

    rs_list, rd_list = track_rs_rd_pairs(instr_trace, all_instrs)
    result = {"rs_list" : rs_list, "rd_list" : rd_list}

    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(result))

    print("Most common RS pairs")
    print_pairs(rs_list)
    print("Most common RD pairs")
    print_pairs(rd_list)

if __name__ == "__main__":
    main()