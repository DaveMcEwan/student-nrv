# Parse the insn_pairs.py script output
# Visualise the most frequent pairs and plot in the form of a heatmap

# Input : Instruction pair histogram, output from insn_pairs.py
# Output : Heatmap figure

import sys
import numpy as np
import matplotlib.pyplot as plt


# Function to parse the instruction pairs and their counters
def parse_pairs_heatmap(pairs_histogram, size):
    all_pairs = {}
    # Getting 5 unique leading and following instructions for the axes
    leading_labels = []
    unique_leading = 0
    following_labels = []
    unique_following = 0
    
    # Iterate through all pairs, form the main dictionary and acquire the n initial unique
    #   leading and following instructions
    for pairs in pairs_histogram:
        words = pairs.split()
        all_pairs[words[0] + " " + words[1][:-1]] = int(words[2]) # Append to dictionary
        lead_instr = words[0][:-1]
        following_instr = words[1][:-1]
        
        if (unique_leading < size and lead_instr not in leading_labels):
            unique_leading += 1
            leading_labels.append(lead_instr)
        
        if (unique_following < size and following_instr not in following_labels):
            unique_following += 1
            following_labels.append(following_instr)

    print(leading_labels)
    print(following_labels)

    # Form the numpy array to be plotted on the heatmap
    arr = np.zeros((size, size), int)
    for y in enumerate(leading_labels):
        for x in enumerate(following_labels):
            key_string = y[1]+", "+x[1]
            if (all_pairs.get(key_string, 0) != 0):
                arr[y[0]][x[0]] = all_pairs[key_string]

    return arr, leading_labels, following_labels

# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def plot_heatmap(arr, y_labels, x_labels):
    print(y_labels)
    print(x_labels)
    fig, ax = plt.subplots()

    im = ax.imshow(arr)

    plt.ylabel('Leading instructions')
    plt.yticks(np.arange(len(y_labels)), y_labels)
    plt.xlabel('Following instructions')
    plt.xticks(np.arange(len(x_labels)), x_labels)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
        rotation_mode="anchor")

    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, arr[i, j],
                        ha="center", va="center", color="w")

    ax.set_title("Frequency of instruction pairs")
    plt.show()

def main():
    # Read in the stdin and store in the pairs_histogram variable
    pairs_histogram = sys.stdin.readlines()
    arr, x_labels, y_labels = parse_pairs_heatmap(pairs_histogram, 16)
    plot_heatmap(arr, x_labels, y_labels)

if __name__ == "__main__":
    main()