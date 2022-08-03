# Identifying the most common sequences (in the form of patterns) of instructions and
#   register combinations. Contains two different functions:
#       - One that parses the instruction and identfies the specific instruction, 
#       and what each register actually is (which means that we can expand upon this
#       to create more meaningful analysis looking at specific register patterns
#       with instructions)
#       - One that solely just looks at the instruction word string and identifies
#       patterns with these

# Input : Instruction trace
# Output :  -  JSON file giving the list of tuples where each instruction
#   pattern is stored with a counter giving how often that pattern has
#   occured. To then be passed into display files. (Optional)
#           -  Formatted list giving the instruction patterns and a counter 
#   detailing how often they've appeared.

# Example to guide use:
# Run the command : python3 scripts/reg_sequences/insn_reg_patterns.py \
# -j=<Output JSON file dump>
# < scripts/example-printf.trc
#   while in the base directory

import sys
import argparse
import os
import json

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("-j", "--jsondump", help="Filepath/name for the JSON files")
parser.add_argument("-r", "--rawdump", help="Filepath/name (without a file extension) \
    for the formatted unfiltered output patterns (prior to identifying the local \
    maxima). Two files are produced from this : a readable .txt file and a .JSON file")
args = parser.parse_args() # ISA argument stored in args.isa

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common.isa_management import check_isa
from common.helper_functions import append_to_counter_dict
from common.reg_functions import parse_instruction
from common.pattern_detection import local_maxima, print_pairs

# Function that parses register information in case we want to expand upon this
#   and look at further information when looking at patterns e.g. specific combinations of
#   instructions and registers
def track_all_insn_patterns(instr_trace, window_size, all_instrs):
    pattern_dict = {}
    window = []

    # Initialise the first window
    for i in range(window_size):
        line = instr_trace[i].split()
        insn = line[4]
        insn_string = insn
        rs1, rs2, rd = parse_instruction(line[4:], all_instrs)

        if rs1:
            insn_string += " rs1[" + rs1 + "]"
            if rs2:
                insn_string += " rs2[" + rs2 + "]"
        if rd:
            insn_string += " rd[" + rd + "]"
        window.append(insn_string)

    key_string = ', '.join(window)
    append_to_counter_dict(pattern_dict, key_string)

    # Iterate through the rest of the window
    for line in instr_trace[window_size:]:
        line_list = line.split()
        insn = line_list[4]
        insn_string = insn
        rs1, rs2, rd = parse_instruction(line_list[4:], all_instrs)

        if rs1:
            insn_string += " rs1[" + rs1 + "]"
            if rs2:
                insn_string += " rs2[" + rs2 + "]"
        if rd:
            insn_string += " rd[" + rd + "]"

        window.append(insn_string)
        window = window[1:]
        key_string = ', '.join(window)
        append_to_counter_dict(pattern_dict, key_string)
    
    return pattern_dict

# Function that just ignores parsing any register information and does it in
#   simplest way possible
def track_all_insn_patterns_simple(instr_trace, window_size):
    patterns_dict = {}
    window = []

    window = [x[34:-1] for x in instr_trace[:window_size]]
    patterns_dict[', '.join(window)] = 1

    for line in instr_trace[window_size:]:
        window.append(line[34:-1])
        window = window[1:]
        append_to_counter_dict(patterns_dict, ', '.join(window))
    
    return patterns_dict

def main():
    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()

    all_patterns_dict = {}

    min_pattern_size = 3
    max_pattern_size = 8
    for i in range(min_pattern_size, max_pattern_size):
        all_patterns_dict.update(track_all_insn_patterns_simple(instr_trace, i))

    # Optional raw information prior to the local maxima calculations can
    #   be saved and stored in their own files
    if args.rawdump:
        raw_result = sorted(all_patterns_dict.items(), key=lambda x: x[1], reverse=True)
        with open(args.rawdump+".JSON", 'w') as dump:
            dump.write(json.dumps(raw_result))
        with open(args.rawdump+".txt", 'w') as dump:
            dump.write("Raw instruction + reg patterns counters\n")
            dump.write(json.dumps(print_pairs(raw_result, dump)))

    minimum_count = 1
    diff_threshold = 5
    result = local_maxima(all_patterns_dict, minimum_count, diff_threshold, False)

    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(result))

    print("Filtered most common instruction+reg patterns")
    print_pairs(result)

if __name__ == "__main__":
    main()