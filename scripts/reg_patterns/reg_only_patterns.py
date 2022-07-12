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
import numpy as np
import matplotlib.pyplot as plt
from numpy import diff

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # ISA argument stored in args.isa

# https://www.geeksforgeeks.org/python-import-from-parent-directory/
# Path adjusting to be able to append helper functions from scripts/
import os
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

# Helper function that checks if an item is in the input dictionary and increments
#   if it is or creates a key if it doesn't exist
def append_to_counter_dict(dict, insn_name):
    if(insn_name in dict):
        dict[insn_name] += 1
    else:
        dict[insn_name] = 1

def track_rs_patterns(instr_trace, window_size, all_instrs):
    rs_pattern_dict = {}
    window = []

    counter = 0
    # Initialise window
    while len(window) != window_size:
        line = instr_trace[counter]
        rs1, rs2, _ = hlp.parse_instruction(line.split()[2:], all_instrs)

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
        rs1, rs2, _ = hlp.parse_instruction(line.split()[2:], all_instrs)

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
        _, _, rd = hlp.parse_instruction(line.split()[2:], all_instrs)

        if rd:
            window.append(rd)
            if len(window) == window_size: # Full window
                append_to_counter_dict(rd_pattern_dict, tuple(window))

        counter += 1

    for line in instr_trace[counter:]:
        _, _, rd = hlp.parse_instruction(line.split()[2:], all_instrs)

        if rd:
            window.append(rd)
            window = window[1:]
            append_to_counter_dict(rd_pattern_dict, tuple(window))

    return sorted(rd_pattern_dict.items(), key=lambda x: x[1], reverse=True)


# Function that takes in the dictionary of all patterns and locates the local maxima
#   by filtering patterns that don't occur frequently, sorting the dictionary
#   and then differentiating with respect to 1. Any differentiated values above 
#   a threshold are then used to indicate which indices to select as the most frequent
#   patterns from the overall dictionary.
# Returns a list of tuples containing the most frequent patterns and their counters
def local_maxima(all_patterns_dict, min, diff_threshold, plot):
    # List comprehension to filter out patterns smaller than a certain counter value
    filtered_patterns = {k:r for k, r in all_patterns_dict.items() if r > min}
    # sorted() returns a list
    sorted_patterns_list = sorted(filtered_patterns.items(), key=lambda x: x[1], reverse=True)
    sorted_patterns = dict(sorted_patterns_list)

    # Differentiate the sorted dictionary values
    dy = np.append(abs(diff(list(sorted_patterns.values()))/1), 0)

    # Initialise with the largest value in the patterns list
    maxima = [sorted_patterns_list[0]]
    # If the current value is above the threshold, add the next index to the return list
    for index, x in enumerate(dy):
        if x > diff_threshold and index < len(dy)-1: # Append next index in patterns list
            maxima.append(sorted_patterns_list[index+1])

    if (plot):
        visualise_indices(sorted_patterns, dy, diff_threshold)

    return maxima

def visualise_indices(sorted_patterns, dy, diff_threshold):
    maximum_indices = np.array([True if x > diff_threshold else False for x in dy][:-1])
    maximum_indices = np.insert(maximum_indices, 0, True)

    # Plot the sorted list
    plt.bar(range(len(sorted_patterns)), list(dict(sorted_patterns).values()))

    # Also plot these indexes on the same graph to see how the values align to
    #   the instruction patterns
    plt.bar(range(len(sorted_patterns)), maximum_indices)
    plt.show()


# Takes in the list of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    for pair in sorted_pairs:
        print(f'{f"{pair[0]}":<32} {str(pair[1])}')

def main():
    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    rs_patterns_dict = {}
    rd_patterns_dict = {}

    for i in range(3, 8):
        rs_patterns_dict.update(track_rs_patterns(instr_trace, i, all_instrs))
        rd_patterns_dict.update(track_rd_patterns(instr_trace, i, all_instrs))

    print("Most common rs access sequences")
    print_pairs(local_maxima(rs_patterns_dict, 5, 10, False))
    print("Most common rd writing sequences")
    print_pairs(local_maxima(rd_patterns_dict, 5, 10, False))

if __name__ == "__main__":
    main()