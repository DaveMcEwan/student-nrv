# Identifying the most common sequences (in the form of patterns) where 
#   registers are read from (rs) or written to (rd)

# Input : Trimmed down instruction trace
# Output : - stdout : Filtered list of the most common register sequences
#   (both rs and rd)
#          - JSON file containing the filtered results stored in the file
#   given by the -j command flag
#          - JSON and txt file containing the raw results, file name given
#   by -r command flag

# Example to guide use:
# Run the command : python3 scripts/reg_patterns/reg_patterns.py \
#       --isa=rv32ic -j=<JSON file output path> \
#       -r=<Raw files output path>
#       < scripts/example-printf.trc
#   while in the base directory

import sys
import argparse
import os
import json

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--isa", help="RISC-V ISA string")
parser.add_argument("-j", "--jsondump", help="Filepath/name for output JSON files")
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

def track_rs_patterns(instr_trace, window_size, all_instrs):
    rs_pattern_dict = {}
    window = []

    counter = 0
    # Initialise window
    while len(window) != window_size:
        line = instr_trace[counter]
        rs1, rs2, _ = parse_instruction(line.split()[4:], all_instrs)

        if rs1:
            window.append(rs1)
            if rs2:
                if len(window) == window_size: # Full window
                    append_to_counter_dict(rs_pattern_dict, tuple(window))
                    window.append(rs2)
                    window = window[1:]
                    append_to_counter_dict(rs_pattern_dict, tuple(window))
                else:
                    window.append(rs2)
                    if len(window) == window_size:
                        append_to_counter_dict(rs_pattern_dict, tuple(window))

        counter += 1

    for line in instr_trace[counter:]:
        rs1, rs2, _ = parse_instruction(line.split()[4:], all_instrs)

        if rs1:
            window.append(rs1)
            window = window[1:]
            append_to_counter_dict(rs_pattern_dict, tuple(window))
            if rs2:
                window.append(rs2)
                window = window[1:]
                append_to_counter_dict(rs_pattern_dict, tuple(window))

    return sorted(rs_pattern_dict.items(), key=lambda x: x[1], reverse=True)

def track_rd_patterns(instr_trace, window_size, all_instrs):
    rd_pattern_dict = {}
    window = []

    counter = 0
    # Initialise window
    while len(window) != window_size:
        line = instr_trace[counter]
        _, _, rd = parse_instruction(line.split()[4:], all_instrs)

        if rd:
            window.append(rd)
            if len(window) == window_size: # Full window
                append_to_counter_dict(rd_pattern_dict, tuple(window))

        counter += 1

    for line in instr_trace[counter:]:
        _, _, rd = parse_instruction(line.split()[4:], all_instrs)

        if rd:
            window.append(rd)
            window = window[1:]
            append_to_counter_dict(rd_pattern_dict, tuple(window))

    return sorted(rd_pattern_dict.items(), key=lambda x: x[1], reverse=True)

def track_rs_rd_patterns(instr_trace, window_size, all_instrs):
    rs_pattern_dict, rd_pattern_dict = {}, {}
    rs_window, rd_window = [], []

    counter = 0
    # Fill initial windows
    while len(rs_window) != window_size or len(rd_window) != window_size:
        line = instr_trace[counter]
        rs1, rs2, rd = parse_instruction(line.split()[4:], all_instrs)
        # Debugging
        # print(line)
        # if rs1: 
        #     print("rs1:"+rs1)
        # if rs2:
        #     print("rs2:"+rs2)
        # if rd:
        #     print("rd:"+rd)
        # print()

        if rs1:
            rs_window.append(rs1)
            if len(rs_window) == window_size + 1:
                rs_window = rs_window[1:]
            if len(rs_window) == window_size:
                append_to_counter_dict(rs_pattern_dict, tuple(rs_window))
            
            if rs2:
                rs_window.append(rs2)
                if len(rs_window) == window_size + 1:
                    rs_window = rs_window[1:]
                if len(rs_window) == window_size:
                    append_to_counter_dict(rs_pattern_dict, tuple(rs_window))

        if rd:
            rd_window.append(rd)
            if len(rd_window) == window_size + 1:
                rd_window = rd_window[1:]
            if len(rd_window) == window_size:
                append_to_counter_dict(rd_pattern_dict, tuple(rd_window))

        counter += 1

    for line in instr_trace[counter:]:
        rs1, rs2, rd = parse_instruction(line.split()[4:], all_instrs)

        if rs1:
            rs_window.append(rs1)
            rs_window = rs_window[1:]
            append_to_counter_dict(rs_pattern_dict, tuple(rs_window))
            if rs2:
                rs_window.append(rs2)
                rs_window = rs_window[1:]
                append_to_counter_dict(rs_pattern_dict, tuple(rs_window))
        if rd:
            rd_window.append(rd)
            rd_window = rd_window[1:]
            append_to_counter_dict(rd_pattern_dict, tuple(rd_window))

    sorted_rs = sorted(rs_pattern_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_rd = sorted(rd_pattern_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_rs, sorted_rd

def main():
    minimum_count = 1
    diff_threshold = 5

    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    rs_patterns_dict = {}
    rd_patterns_dict = {}

    for i in range(3, 8):
        rs, rd = track_rs_rd_patterns(instr_trace, i, all_instrs)
        
        rs_patterns_dict.update(rs)
        rd_patterns_dict.update(rd)
        # rs_patterns_dict.update(track_rs_patterns(instr_trace, i, all_instrs))
        # rd_patterns_dict.update(track_rd_patterns(instr_trace, i, all_instrs))

    if args.rawdump:
        raw_result = {}
        raw_rs_patterns = sorted(rs_patterns_dict.items(), key=lambda x: x[1], reverse=True)
        raw_rd_patterns = sorted(rd_patterns_dict.items(), key=lambda x: x[1], reverse=True)
        raw_result["raw_rs"] = raw_rs_patterns
        raw_result["raw_rd"] = raw_rd_patterns
        with open(args.rawdump+".JSON", 'w') as dump:
            dump.write(json.dumps(raw_result))
        with open(args.rawdump+".txt", 'w') as dump:
            dump.write("Raw most common patterns of 'rs' accesses")
            dump.write(print_pairs(raw_rs_patterns, dump))
            dump.write("Raw most common patterns of 'rd' accesses")
            dump.write(print_pairs(raw_rd_patterns, dump))

    filtered_result = {}
    filtered_rs_patterns = local_maxima(rs_patterns_dict, minimum_count, diff_threshold, False)
    filtered_rd_patterns = local_maxima(rd_patterns_dict, minimum_count, diff_threshold, False)
    filtered_result["filtered_rs"] = filtered_rs_patterns
    filtered_result["filtered_rd"] = filtered_rd_patterns

    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(filtered_result))

    print("Most common rs access sequences")
    print_pairs(filtered_rs_patterns)
    print("Most common rd writing sequences")
    print_pairs(filtered_rd_patterns)

if __name__ == "__main__":
    main()