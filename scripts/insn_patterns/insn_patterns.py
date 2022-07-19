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

# Function that takes in the dictionary of all patterns and locates the local maxima
#   by filtering patterns that don't occur frequently, sorting the dictionary
#   and then differentiating with respect to 1. Any differentiated values above 
#   a threshold are then used to indicate which indices to select as the most frequent
#   patterns from the overall dictionary.
# Returns a list of tuples containing the most frequent patterns and their counters
def local_maxima(all_patterns_dict, min, diff_threshold, plot):
    # List comprehension to filter out patterns smaller than a certain counter value
    filtered_patterns = {k:r for k, r in all_patterns_dict.items() if r > min}

    print("Minimum Count: "+str(min)+", Differentiation threshold: "+str(diff_threshold))

    if not filtered_patterns:
        print("No pattern has occured more often than the set minimum: "+str(min))
        print("Change this value in scripts/insn_patterns/insn_patterns.py")
        return []
    
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
    
    if not maxima:
        print("No local maxima detected; it may be that the set differentiation\
            threshold :"+str(diff_threshold)+", is too high to detect a local maxima. \
            Adjust this in scripts/insn_patterns/insn_patterns.py")

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

def print_pairs(sorted_pairs):
    for pair in sorted_pairs:
        stripped_key = str(pair[0])[1:-1].replace("'","")
        print(f'{f"{stripped_key}":<32} {str(pair[1])}')

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
    print_pairs(maxima)
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

    # print_pairs(all_patterns_dict)
    print_pairs(local_maxima(all_patterns_dict, minimum_count, diff_threshold, False))

if __name__ == "__main__":
    main()