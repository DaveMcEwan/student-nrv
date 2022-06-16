# Parse the insn_pairs.py script output
# Visualise the most frequent pairs and plot in the form of a bar graph

import sys
import matplotlib.pyplot as plt

# Function to parse the instruction pairs and their counters into a format
#   that can be plotted into a bar chart easily
def parse_pairs_bar(pairs_histogram, n):
    popular_pairs = {}
    counter = 0
    for pairs in pairs_histogram:
        if (counter == n):
            break
        else:
            counter += 1
            words = pairs.split()
            popular_pairs[words[0] + " " + words[1][:-1]] = int(words[2])

    return popular_pairs

def plot_bar(popular_pairs):
    plt.bar(range(len(popular_pairs)), list(popular_pairs.values()))
    plt.xticks(range(len(popular_pairs)), list(popular_pairs.keys()))
    plt.xticks(rotation=45)
    plt.show()

def main():
    # Read in the stdin and store in the pairs_histogram variable
    pairs_histogram = sys.stdin.readlines()
    plot_bar(parse_pairs_bar(pairs_histogram, 20))

if __name__ == "__main__":
    main()