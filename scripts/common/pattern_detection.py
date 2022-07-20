import numpy as np
import matplotlib.pyplot as plt
from numpy import diff
import sys

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
def print_pairs(sorted_pairs, stream=sys.stdout):
    for pair in sorted_pairs:
        print(f'{f"{pair[0]}":<48} {str(pair[1])}', file=stream)