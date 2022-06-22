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
import time

#   Iterate through the instruction stream and calculate the most frequent
#       instruction patterns of size n
def track_patterns(instr_trace, n):
    patterns_dict = {}
    window = [0]*n # Empty list to represent the moving window looking for patterns

    # Set up the first window
    for i in range(n):
        window[i] = instr_trace[i].split()[1]
    patterns_dict[tuple(window)] = 1

    # Iterate through the rest of the instructions
    for line in instr_trace[n:]:
        insn_name = line.split()[1]

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

    # Form a mask of True and Falses indicating where the peak value of that region is
    #   Also popping the end of the list to shift the values forward so that
    #   the 'True's correspond with the maximum value in a section
    maximum_indices = np.array([True if x > diff_threshold else False for x in dy][:-1])

    # Insert True at the very start since the pattern that appeared the most
    #   is definitely part of the list
    maximum_indices = np.insert(maximum_indices, 0, True)

    return_list =[]
    for index in enumerate(maximum_indices):
        if (index[1]):
            return_list.append(sorted_patterns_list[index[0]])

    return return_list
    # Grab the instruction tuples which the indices align with
    masked_values = np.array(list(sorted_patterns))[maximum_indices]

    # Optional bool to plot to therefore allow a user to visualise which local
    #   maxima was selected - allows the user to verify that the local maxima was selected
    if (plot):
        # Plot the sorted list
        plt.bar(range(len(sorted_patterns)), list(dict(sorted_patterns).values()))

        # Also plot these indexes on the same graph to see how the values align to
        #   the instruction patterns
        plt.bar(range(len(sorted_patterns)), maximum_indices)
        plt.show()

    # Return the dictionary values (frequency counters) 
    return ({key:filtered_patterns.get(key) for key in masked_values}).items()

# Takes in a dictionary and prints out the pairs and counters in a readable way
# def print_pairs(sorted_pairs):
#     for k, v in sorted_pairs.items():
#         # Remove brackets and apostrophes
#         stripped_key = str(k)[1:-1].replace("'","")
#         # Print in a formaatted manner
#         print(f'{stripped_key:<64} {str(v)}')

def print_pairs(sorted_pairs):
    for pair in sorted_pairs:
        stripped_key = str(pair[0])[1:-1].replace("'","")
        print(f'{f"{stripped_key}":<32} {str(pair[1])}')

def main():
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
    print_pairs(maxima)
    end_time = time.time()
    print("Time taken to print = "+str(end_time-start_time))

if __name__ == "__main__":
    main()