# Display script used for visualising the register access distribution.

# Input : JSON file provided by the reg_accesses.py script.
# Output : Several figures plotted using Matplotlib visualising the distribution
#   per register type.

import argparse
from cProfile import label
import json
from re import S
import matplotlib.pyplot as plt

# Input argument parsing (to detect the input filepath)
parser = argparse.ArgumentParser()
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # Filepath argument stored in args.filedump

# Function used to take a general counter list in and plot bar columns
def display_general_barchart(name, counter_list):
    if not isinstance(counter_list, list):
        return

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
    elif name == "address_offset":
        plt.title("Most frequent address offset values")
        plt.xlabel("Immediates (Offsets)")
        plt.ylabel("Number of times used")
    elif name == "branch_offset":
        plt.title("Most frequent branch offsets values")
        plt.xlabel("Immediates (Branch offsets)")
        plt.ylabel("Number of times used")
    elif name == "shift":
        plt.title("Most frequent shift values")
        plt.xlabel("Immediates (Shifts)")
        plt.ylabel("Number of times used")
    elif name == "arith":
        plt.title("Most frequent arithmetic values")
        plt.xlabel("Immediates (Arithmetic values)")
        plt.ylabel("Number of times used")
    
    plt.show()

# Function used to see how much each register available in the system was used as a source or destination register
def reg_distribution_plot(all_regs):
    reg_names = [x[0] for x in all_regs]
    rs_list = [x[1]["rs"] for x in all_regs]
    rd_list = [x[1]["rd"] for x in all_regs]

    plt.bar(range(len(reg_names)), height=rs_list, width=0.4, align='edge', label="rs")
    plt.bar(range(len(reg_names)), height=rd_list, width=-0.4, align='edge', label="rd")

    plt.xticks(range(len(reg_names)), reg_names)
    plt.xlabel("Registers")
    plt.ylabel("Frequency")
    plt.legend()

    plt.show()

# Visualise the distribution of the immediates and what they are used for
def imm_distribution_plot(off, branch_off, shift, arith):
    sums_list = [0]*4
    sums_list[0] = sum(i for _,i in off)
    sums_list[1] = sum(i for _,i in branch_off)
    sums_list[2] = sum(i for _,i in shift)
    sums_list[3] = sum(i for _,i in arith)
    sums_list = sorted(sums_list, reverse=True)

    plt.bar(range(len(sums_list)), sums_list)
    plt.xticks(range(len(sums_list)), ["Immediate total", "Address offsets", 
        "Branch offsets", "Shift", "Arithmetic"])
    plt.title("Immediate distribution of "+str(sum(sums_list))+" immediates")
    plt.xlabel("Immediate type")
    plt.ylabel("Frequency")
    plt.show()

def main():
    # Read in the associated lists and store in the data dictionary
    with open('scripts/reg_accesses/test-rs.txt', 'r') as dump:
        data = json.load(dump)

    # Visualise distribution of immediates (What the immediates are used for)
    imm_distribution_plot(data["address_offset"], data["branch_offset"], 
        data["shift"], data["arith"])

    all_regs = list(data["all_regs"].items())
    # Visualise the distribution of the registers with what they are used as (rs and rd)
    reg_distribution_plot(all_regs)

    rs_list = [[x[0], x[1]["rs"]] for x in all_regs if x[1]["rs"] > 0]
    sorted_rs_list = sorted(rs_list, key=lambda x: x[1], reverse=True)
    # Plot the general bar chart giving the most popular regs used as source regs
    display_general_barchart("rs", sorted_rs_list)

    rd_list = [[x[0], x[1]["rd"]] for x in all_regs if x[1]["rd"] > 0]
    sorted_rd_list = sorted(rd_list, key=lambda x: x[1], reverse=True)
    # Plot the general bar chart giving the most popular regs used as dest regs
    display_general_barchart("rd", sorted_rd_list)

    # Iterate through the dictionary and plot general bar column graphs for them
    for k, v in data.items():
        display_general_barchart(k, v)

if __name__ == "__main__":
    main()