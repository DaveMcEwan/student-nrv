# Display script used for visualising the register access distribution.

# Input : JSON file provided by the reg_accesses.py script.
# Output : Several figures plotted using Matplotlib visualising the distribution
#   per register type.

# Example to guide use:
# Run the command : python3 scripts/reg_accesses/reg_display.py \
#   --isa=rv32ic -j=<input json file from reg_accesses.py> \
#   --img=<output png prefix>
#   < scripts/example.trc
#   while in the base directory

# Produces multiple figures, each with their own suffix

import argparse
import json
import matplotlib.pyplot as plt

# Input argument parsing (to detect the input filepath)
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jsondump", help="Filepath/name for input JSON files")
parser.add_argument("-i", "--img", help="Filepath/name prefix for the output figure")
args = parser.parse_args()

# Function used to take a general counter list in and plot bar columns
def display_general_barchart(name, counter_list):
    if not isinstance(counter_list, list):
        return

    l_size = len(counter_list) if len(counter_list) < 10 else 10
    keys = [x[0] for x in counter_list[:l_size]]
    counters = [x[1] for x in counter_list[:l_size]]

    plt.figure()
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
    
    plt.savefig(args.img+"_"+name)

# Function used to see how much each register available in the system was used as a source or destination register
def reg_distribution_plot(all_regs):
    reg_names = [x[0] for x in all_regs]
    rs_list = [x[1]["rs"] for x in all_regs]
    rd_list = [x[1]["rd"] for x in all_regs]

    plt.figure()
    plt.bar(range(len(reg_names)), height=rs_list, width=0.4, align='edge', label="rs")
    plt.bar(range(len(reg_names)), height=rd_list, width=-0.4, align='edge', label="rd")

    plt.xticks(range(len(reg_names)), reg_names)
    plt.xlabel("Registers")
    plt.ylabel("Frequency")
    plt.legend()

    plt.savefig(args.img+"_dist")

def main():
    # Read in the associated lists and store in the data dictionary
    with open(args.jsondump, 'r') as dump:
        data = json.load(dump)

    # data is the dictionary storing the the registers and their counters
    #   which determine how often they've been used as a specific register.

    all_regs = list(data.items())
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

if __name__ == "__main__":
    main()