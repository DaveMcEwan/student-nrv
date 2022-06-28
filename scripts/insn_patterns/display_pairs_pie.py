# Parse the insn_pairs.py script output
# Visualise the most frequent pairs and plot in the form of a pie chart

# Input : Instruction pair histogram, output from insn_pairs.py
# Output : Pie chart

import sys
import matplotlib.pyplot as plt

# Function to parse the instruction pairs and their counters into a format
#   that can be plotted into a bar chart easily; same as the one used in the bar chart script
def parse_pairs_pie(pairs_histogram, n):
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

def plot_pie(popular_pairs):
    plt.pie(list(popular_pairs.values()), labels=list(popular_pairs.keys()), autopct='%1.1f%%')
    plt.show()

def main():
    # Read in the stdin and store in the pairs_histrogram variable
    pairs_histogram = sys.stdin.readlines()
    popular_pairs = parse_pairs_pie(pairs_histogram, 10)
    plot_pie(popular_pairs)

if __name__ == "__main__":
    main()