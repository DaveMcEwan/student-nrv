# Take an input list of tuples where each tuple consists of an independent
#   variable (to be placed on the x-axis) along with a dependent variable
#   (to be placed on the y-axis) and plots this on a column graph using
#   matplotlib

# Input : JSON file containing the input list of tuples
# Output : Figure in the form of a .pdf file saved in the 
#   file path provided by the --filepath python argument.

# Example to guide use:
# Run the command : python3 scripts/common/display/column.py \
#                   -j=<optional json file path> \
#                   < scripts/example-printf.trc
#   while in the base directory

import matplotlib.pyplot as plt
import json
import argparse

# Input argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jsondump", help="Filepath/name for output JSON files")
parser.add_argument("-p", "--profile", help="Display profile, choose from: \
    insn_pairs, insn_patterns or leave empty for default title/axis names")
parser.add_argument("-f", "--filepath", help="Filepath/name for the saved figure")
args = parser.parse_args()

def plot_bar(data_pairs):
    pairs = [x[0] for x in data_pairs]
    counters = [x[1] for x in data_pairs]
    plt.bar(range(len(data_pairs)), counters)
    plt.xticks(range(len(data_pairs)), pairs)
    plt.xticks(rotation=45)

    # Profiles
    if args.profile == "insn_pairs":
        plt.title("Most common instruction pairs")
        plt.xlabel("Instruction pairs")
        plt.ylabel("Frequency")
    elif args.profile == "insn_patterns":
        plt.title("Most common instruction patterns")
        plt.xlabel("Instruction patterns")
        plt.ylabel("Frequency")
    else:
        plt.title("Column graph")
        plt.xlabel("Independent Variable")
        plt.ylabel("Magnitude")

    plt.savefig(args.filepath)

def main():
    with open(args.jsondump, 'r') as dump:
        data = json.load(dump)

    plot_bar(data)

if __name__ == "__main__":
    main()