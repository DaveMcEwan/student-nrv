# Analyse the instruction trace input through stdin
# Identify the most common instruction pairs

# Input : Trimmed down instruction trace
# Output : Formatted list giving the instruction pairs and a counter 
#   detailing how often they've appeared

# Example to guide use:
# Run the command : python3 scripts/insn_pairs/insn_pairs.py --isa=rv32ic < scripts/example.trc
#   while in the base directory

import sys


#   Iterate through the instruction stream and calculate the most frequent instruction pairs
def track_pairs(instr_trace):
    pairs_dict = {}
    previous_instr = instr_trace[0].split()[1] # Set the first instruction first 

    for line in instr_trace[1:]:
        words = line.split()
        insn_name = words[1]

        key_string = previous_instr+", "+insn_name

        if (pairs_dict.get(key_string, 0) == 0):
            pairs_dict[key_string] = 1
        else:
            pairs_dict[key_string] += 1
        
        previous_instr = insn_name
    
    # Sort based on the corresponding counter values
    sorted_pairs = sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

    # Returns a list of tuples where each instruction is associated with their counter
    return sorted_pairs

# Takes in the list of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    for pair in sorted_pairs:
        print(f'{f"{pair[0]},":<32} {str(pair[1])}')

def main():

    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    print_pairs(track_pairs(instr_trace))

if __name__ == "__main__":
    main()