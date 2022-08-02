# Identifying the most common sequences (in the form of pairs) of instructions and
#   register combinations

# Input : Trimmed down instruction trace
# Output : TODO

# Example to guide use:
# Run the command : python3 scripts/reg_sequences/insn_reg_pairs.py < scripts/example.trc
#   while in the base directory

import sys
import argparse
import os
import json

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("-j", "--jsondump", help="Filepath/name for the JSON files")
args = parser.parse_args() # ISA argument stored in args.isa

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common.isa_management import check_isa
from common.helper_functions import append_to_counter_dict
from common.reg_functions import parse_instruction
from common.pattern_detection import print_pairs

# Measure the most frequent instruction pairs where there is an rs
def track_insn_rs_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    counter = 0
    while not key_string:
        line = instr_trace[counter].split()
        insn = line[4]
        rs1, rs2, _ = parse_instruction(line[4:], all_instrs)

        if rs1:
            key_string = insn + " rs1[" + rs1 + "]"
            if rs2:
                key_string += " rs2[" + rs2 + "]"
            key_string += ", "
        counter += 1

    for line in instr_trace[counter:]:
        line_list = line.split()
        insn = line_list[4]
        rs1, rs2, _ = parse_instruction(line_list[4:], all_instrs)

        # ---- If we want instructions without an rs to NOT BREAK patterns ---- #
        # if rs1:
        #     s_append = insn + " rs1[" + rs1 + "]"
        #     if rs2:
        #         s_append += " rs2[" + rs2 + "]"
        #     append_to_counter_dict(pairs_dict, key_string+s_append)
        #     key_string = s_append + ", "
        
        # ---- If we want instructions without an rs to BREAK patterns ---- #
        if rs1:
            if key_string: # Non-empty string
                s_append = insn + " rs1[" + rs1 + "]"
                if rs2:
                    s_append += " rs2[" + rs2 + "]"
                append_to_counter_dict(pairs_dict, key_string+s_append)

                # Prepare string for next pairing
                key_string = s_append + ", "
            else:  # Empty string
                key_string = insn + " rs1[" + rs1 + "]"
                if rs2:
                    key_string += " rs2[" + rs2 + "]"
                key_string += ", "
        else:
            key_string = ""

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Measure the most frequent instruction pairs where there is an rd
def track_insn_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    counter = 0
    while not key_string:
        line = instr_trace[counter].split()
        insn = line[4]
        _, _, rd = parse_instruction(line[4:], all_instrs)

        if rd:
            key_string = insn + " rd[" + rd + "], "
        
        counter += 1

    for line in instr_trace[counter:]:
        line_list = line.split()
        insn = line_list[4]
        _, _, rd = parse_instruction(line_list[4:], all_instrs)

        # ---- If we want instructions without an rd to NOT BREAK patterns ---- #
        # if rd:
        #     s_append = insn + " rd[" + rd + "]"
        #     append_to_counter_dict(pairs_dict, key_string+s_append)
        #     key_string = s_append + ", "
        
        # ---- If we want instructions without an rd to BREAK patterns ---- #
        if rd:
            s_append = insn + " rd[" + rd + "]"
            if key_string:
                append_to_counter_dict(pairs_dict, key_string+s_append)
            
            key_string  = s_append + ", "
        else:
            key_string = ""
        

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Measure the most frequent instruction pairs where there is either an rs or rd
def track_insn_rs_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    counter = 0
    while not key_string:
        line = instr_trace[counter].split()
        insn = line[4]
        rs1, rs2, rd = parse_instruction(line[4:], all_instrs)

        if rs1:
            key_string = insn + " rs1[" + rs1 + "]"
            if rs2:
                key_string += " rs2[" + rs2 + "]"
        
        if rd:
            if key_string:
                key_string += " rd[" + rd + "]"
            else:
                key_string = insn + " rd[" + rd + "]"
        
        if key_string:
            key_string += ", "

        counter += 1

    for line in instr_trace[counter:]:
        line_list = line.split()
        insn = line_list[4]
        rs1, rs2, rd = parse_instruction(line_list[4:], all_instrs)

        # ---- If we want instructions without an rs/rd to NOT BREAK patterns ---- #
        # s_append = ""
        # if rs1:
        #     s_append += insn + " rs1[" + rs1 + "]"
        #     if rs2:
        #         s_append += " rs2[" + rs2 + "]"

        # if rd:
        #     if s_append:
        #         s_append += " rd[" + rd + "]"
        #     else:
        #         s_append = insn + " rd[" + rd "]"
        
        # if s_append:
        #     append_to_counter_dict(pairs_dict, key_string+s_append)
        #     key_string = s_append

        # ---- If we want instructions without an rs/rd to BREAK patterns ---- #
        # Must account for key_string potentially being empty

        empty = False if key_string else True

        s_append = ""
        if rs1:
            s_append += insn + " rs1[" + rs1 + "]"
            if rs2:
                s_append += " rs2[" + rs2 + "]"

        if rd:
            if not s_append:
                s_append += insn

            s_append += " rd[" + rd + "]"
        
        if s_append:
            if not empty:
                append_to_counter_dict(pairs_dict, key_string+s_append)
            key_string = s_append + ", "
        else:
            key_string = ""

        # ---- If we want instructions without an rs to BE INCLUDED IN patterns ---- #
        # Requires a separate function since the initialisation is different
        #   See track_all_insn_pairs()

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Function used to track the most frequent instruction + (registers) patterns regardless
#   on whether or not there are registers associated with that instruction
def track_all_insn_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    # Initialise with the first instruction only
    line = instr_trace[0].split()
    insn = line[4]
    rs1, rs2, rd = parse_instruction(line[4:], all_instrs)

    key_string = insn
    if rs1:
        key_string += " rs1[" + rs1 + "]"
        if rs2:
            key_string += " rs2[" + rs2 + "]"
        
    if rd:
        key_string += " rd[" + rd + "]"
    
    key_string += ", "

    # Iterate through the rest of the instructions
    for line in instr_trace[1:]:
        line_list = line.split()
        insn = line_list[4]
        rs1, rs2, rd = parse_instruction(line_list[4:], all_instrs)

        s_append = insn
        if rs1:
            s_append += " rs1[" + rs1 + "]"
            if rs2:
                s_append += " rs2[" + rs2 + "]"

        if rd:
            s_append += " rd[" + rd + "]"
        
        append_to_counter_dict(pairs_dict, key_string+s_append)
        key_string = s_append + ", "
    
    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

def main():
    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()

    result = track_all_insn_pairs(instr_trace, all_instrs)
    
    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(result))

    print_pairs(result)

if __name__ == "__main__":
    main()