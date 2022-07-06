# Display script used for visualising the register access distribution.

# Input : JSON file provided by the reg_accesses.py script.
# Output : Several figures plotted using Matplotlib visualising the distribution
#   per register type.

import argparse
import json
import matplotlib.pyplot as plt

# Input argument parsing (to detect the input filepath)
parser = argparse.ArgumentParser()
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # Filepath argument stored in args.filedump

# Function used to take a general counter list in and plot bar columns
def display_general_barchart(name, counter_list):
    l_size = len(counter_list) if len(counter_list) < 10 else 10
    keys = [x[0] for x in counter_list[:l_size]]
    counters = [x[1] for x in counter_list[:l_size]]

    plt.bar(range(l_size), counters)
    plt.xticks(range(l_size), keys)
    if len(counters):
        plt.yticks(range(counters[0] + 1))
    else: # Case for empty lists
        plt.yticks([0, 1])
    
    if name == "rs":
        plt.title("Registers used most frequently as source registers")
        plt.xlabel("Registers")
        plt.ylabel("Number of times accessed")
    elif name == "rd":
        plt.title("Registers used most frequently as destination registers")
        plt.xlabel("Registers")
        plt.ylabel("Number of times read to")
    elif name == "imm":
        plt.title("Most frequent immediate values")
        plt.xlabel("Immediates")
        plt.ylabel("Number of times used")
    elif name == "offset_dict":
        plt.title("Most frequent address offset values")
        plt.xlabel("Immediates (Offsets)")
        plt.ylabel("Number of times used")
    elif name == "branch_offset":
        plt.title("Most frequent branch offsets values")
        plt.xlabel("Immediates (Branch offsets)")
        plt.ylabel("Number of times used")
    elif name == "shift_dict":
        plt.title("Most frequent shift values")
        plt.xlabel("Immediates (Shifts)")
        plt.ylabel("Number of times used")
    elif name == "arith_dict":
        plt.title("Most frequent arithmetic values")
        plt.xlabel("Immediates (Arithmetic values)")
        plt.ylabel("Number of times used")
    
    plt.show()

def main():
    # Read in the associated lists and store in the data dictionary
    with open('scripts/reg_accesses/test-rs.txt', 'r') as dump:
        data = json.load(dump)

    # Iterate through the dictionary and plot general bar column graphs for them
    for k, v in data.items():
        display_general_barchart(k, v)

if __name__ == "__main__":
    main()