# Analyse the instruction trace input through stdin
# Identify the most common instruction patterns (sequences of n instructions)

# Input : Trimmed down instruction trace
# Output :  -  JSON file giving the list of tuples where each instruction
#   pattern is stored with a counter giving how often that pattern has
#   occured. To then be passed into display files. (Optional)
#           -  Formatted list giving the instruction patterns and a counter 
#   detailing how often they've appeared.

# Example to guide use:
# Run the command : python3 scripts/insn_patterns/insn_patterns.py \
#                   -j=<optional json file path> \
#                   < scripts/example-printf.trc
#   while in the base directory

import sys
import time
import json
import os
import argparse

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Function to calculate the local maxima among groups of values
from common.pattern_detection import local_maxima, print_patterns

# Input argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jsondump", help="Filepath/name for output JSON files")
args = parser.parse_args()

#   Iterate through the instruction stream and calculate the most frequent
#       instruction patterns of size n
def track_patterns(instr_trace, n):
    patterns_dict = {}
    window = [0]*n # Empty list to represent the moving window looking for patterns

    # Set up the first window
    for i in range(n):
        window[i] = instr_trace[i].split()[4]
    patterns_dict[tuple(window)] = 1

    # Iterate through the rest of the instructions
    for line in instr_trace[n:]:
        insn_name = line.split()[4]

        # Push new instruction into the window and pop the element at the 0th index
        window.append(insn_name)
        window = window[1:]

        key_tuple = tuple(window)
        if (key_tuple in patterns_dict):
            patterns_dict[key_tuple] += 1
        else:
            patterns_dict[key_tuple] = 1

    # Returns a dictionary where each instruction pattern is associated with 
    #   their counter   
    return patterns_dict

# Main function with timing in case I want to come back and optimise again
def timed_main():    
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    all_patterns_dict = {}

    start_time = time.time()
    for i in range(3, 8):
        all_patterns_dict.update(track_patterns(instr_trace, i))
    end_time = time.time()
    print("Time taken = "+str(end_time-start_time))

    start_time = time.time()
    maxima = local_maxima(all_patterns_dict, 5, 10, False)
    end_time = time.time()
    print("Time taken to retrieve local maxima = "+str(end_time-start_time))

    start_time = time.time()
    print_patterns(maxima)
    end_time = time.time()
    print("Time taken to print = "+str(end_time-start_time))

# Default main
def main():
    minimum_count = 1
    diff_threshold = 5
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    all_patterns_dict = {}

    for i in range(3, 8):
        all_patterns_dict.update(track_patterns(instr_trace, i))

    result = local_maxima(all_patterns_dict, minimum_count, diff_threshold, False)

    # Dump the list of most common patterns in a .json file to access
    #   it easily in the display scripts
    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(result))

    # Print the formatted version to stdout for user readability
    print_patterns(result)

if __name__ == "__main__":
    main()