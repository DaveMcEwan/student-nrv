# Analyse the instruction trace input through stdin
# Identify the most common instruction patterns (sequences of n instructions)

# Input : Trimmed down instruction trace
# Output : Formatted list giving the instruction patterns and a counter 
#   detailing how often they've appeared

# Example to guide use:
# Run the command : python3 scripts/insn_pairs/insn_patterns.py < scripts/example.trc
#   while in the base directory

import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy import diff

#   Iterate through the instruction stream and calculate the most frequent
#       instruction patterns of size n
def track_patterns(instr_trace, n):
    patterns_dict = {}
    window = [0]*n # Empty list to represent the moving window looking for patterns

    # Set up the first window
    for i in range(n):
        window[i] = instr_trace[i].split()[1]
    
    # previous_instr = instr_trace[0].split()[1] # Set the first instruction first 
    patterns_dict[tuple(window)] = 1

    # Iterate through the rest of the instructions
    for line in instr_trace[n:]:
        words = line.split()
        insn_name = words[1]

        # Push new instruction into the window and pop the element at the 0th index
        window.append(insn_name)
        window.pop(0)

        if (patterns_dict.get(tuple(window), 0) == 0):
            patterns_dict[tuple(window)] = 1
        else:
            patterns_dict[tuple(window)] += 1
    
    # Sort based on the corresponding counter values
    # sorted_pairs = sorted(patterns_dict.items(), key=lambda x: x[1], reverse=True)

    return patterns_dict
    # Returns a list of tuples where each instruction pattern is associated with their counter

# Takes in the LIST of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    for pair in sorted_pairs:
        print_template = ""
        for insn in range(len(pair[0])):
            print_template += pair[0][insn] + ", "
        print(f'{print_template:<64} {str(pair[1])}')


def main():
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    all_patterns_dict = {}

    for i in range(3, 8):
        all_patterns_dict.update(track_patterns(instr_trace, i))

    # List comprehension to filter out patterns smaller than a certain counter value
    filtered_patterns = {k:r for k, r in all_patterns_dict.items() if r > 5}
    sorted_patterns = dict(sorted(filtered_patterns.items(), key=lambda x: x[1], reverse=True))
    # print_pairs(sorted_patterns)

    # Plot the sorted list
    plt.bar(range(len(sorted_patterns)), list(dict(sorted_patterns).values()))

    # Differentiate the sorted dictionary values
    dy = np.append(abs(diff(list(sorted_patterns.values()))/1), 0)

    # Form a mask of True and Falses indicating where the peak value of that region is
    #   Also popping the end of the list to shift the values forward so that
    #   the 'True's correspond with the maximum value in a section
    maximum_indices = np.array([True if x > 10 else False for x in dy][:-1])

    # Insert True at the very start since the pattern that appeared the most
    #   is definitely part of the list
    maximum_indices = np.insert(maximum_indices, 0, True)

    # Also plot these indexes on the same graph to see how the values align to
    #   the instruction patterns
    plt.bar(range(len(sorted_patterns)), maximum_indices)
    plt.show()

    # Grab the instruction patterns which the indices align with
    masked_values = np.array(list(sorted_patterns))[maximum_indices]
    print("Most frequent patterns : " + str(masked_values))

if __name__ == "__main__":
    main()