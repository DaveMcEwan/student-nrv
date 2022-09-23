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
from common.pattern_detection import local_maxima, print_pairs
from common.helper_functions import append_to_counter_dict

# Input argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--seq_length", help="Length of ")
parser.add_argument("-j", "--jsondump", help="Filepath/name for output JSON files")
parser.add_argument("-r", "--rawdump", help="Filepath/name (without a file extension) \
    for the formatted unfiltered output patterns (prior to identifying the local \
    maxima). Two files are produced from this : a readable .txt file and a .JSON file")
args = parser.parse_args()

#   Iterate through the instruction stream and calculate the most frequent
#       instruction patterns of size n
def track_patterns():
    patterns_dict = {}

    # Ideas: - Read in first 8 values by just using readline.
    #   - Do windows up to the 8th value
    #   - Once all windows are aligned on the 8th value, have a single for loop
    #   for the rest of the input values which all windows are adjusted to

    # Initialising the windows between sizes 3 to 8
    window = []
    for i in range(8):
        window.append((sys.stdin.readline().split())[4])

    for i in range(6,1,-1):
        for j in range(i):
            append_to_counter_dict(patterns_dict, ', '.join(window[j:j+(8-i)]))

    # Iterate through the rest of the instructions
    for line in sys.stdin:
        insn_name = line.split()[4]

        # Push new instruction into the window and pop the element at the 0th index
        window.append(insn_name)
        window = window[1:]

        # Concatenate the elements of the window list to form a string which
        #   then acts as a key for the dictionary. Done so that the format matches
        #   that of the pair detection algorithm and because dictionaries can only
        #   take immutable types as keys
        for i in range(6):
            append_to_counter_dict(patterns_dict, ', '.join(window[i:]))

    # Returns a dictionary where each instruction pattern is associated with 
    #   their counter
    return patterns_dict

# Main function with timing in case I want to come back and optimise again
def timed_main():    
    # Read in the stdin and store in the instr_trace variable
    # instr_trace = sys.stdin.readlines()
    all_patterns_dict = {}

    start_time = time.time()
    all_patterns_dict.update(track_patterns())
    end_time = time.time()
    print("Time taken = "+str(end_time-start_time))

    start_time = time.time()
    maxima = local_maxima(all_patterns_dict, 5, 10, False)
    end_time = time.time()
    print("Time taken to retrieve local maxima = "+str(end_time-start_time))

    start_time = time.time()
    print_pairs(maxima)
    end_time = time.time()
    print("Time taken to print = "+str(end_time-start_time))

# Default main
def main():
    minimum_count = 1
    diff_threshold = 5
    all_patterns_dict = {}

    # for i in range(min_pattern_size, max_pattern_size):
    all_patterns_dict.update(track_patterns())

    # Optional raw information prior to the local maxima calculations can
    #   be saved and stored in their own files
    if args.rawdump:
        raw_result = sorted(all_patterns_dict.items(), key=lambda x: x[1], reverse=True)
        with open(args.rawdump+".JSON", 'w') as dump:
            dump.write(json.dumps(raw_result))
        with open(args.rawdump+".txt", 'w') as dump:
            dump.write("Raw most common instruction patterns for sizes \
                between 3 and 8")
            dump.write(json.dumps(print_pairs(raw_result, dump)))

    result = local_maxima(all_patterns_dict, minimum_count, diff_threshold, False)

    # Dump the list of most common patterns in a .json file to access
    #   it easily in the display scripts
    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(result))

    # Print the formatted version to stdout for user readability
    print("Filtered most common instruction patterns for sizes between \
        3 and 8")
    print_pairs(result)

if __name__ == "__main__":
    main()