# Analyse the instruction trace input through stdin
# Identify the most common instruction patterns (sequences of n instructions)

# Input : Trimmed down instruction trace
# Output : Formatted list giving the instruction patterns and a counter 
#   detailing how often they've appeared

# Example to guide use:
# Run the command : python3 scripts/insn_pairs/insn_patterns.py < scripts/example.trc
#   while in the base directory

import sys

#   Iterate through the instruction stream and calculate the most frequent
#       instruction patterns of size n
def track_patterns(instr_trace, n):
    patterns_dict = {}
    window = [0]*n # Empty list to represent the moving window looking for patterns

    # Set up the first window
    for i in range(n):
        window[i] = instr_trace[i].split()[1]
    
    # previous_instr = instr_trace[0].split()[1] # Set the first instruction first 
    patterns_dict[tuple(window)] = 1

    # Iterate through the rest of the instructions
    for line in instr_trace[n:]:
        words = line.split()
        insn_name = words[1]

        # Push new instruction into the window and pop the element at the 0th index
        window.append(insn_name)
        window.pop(0)

        if (patterns_dict.get(tuple(window), 0) == 0):
            patterns_dict[tuple(window)] = 1
        else:
            patterns_dict[tuple(window)] += 1
    
    # Sort based on the corresponding counter values
    # sorted_pairs = sorted(patterns_dict.items(), key=lambda x: x[1], reverse=True)

    return patterns_dict
    # Returns a list of tuples where each instruction pattern is associated with their counter

# Takes in the list of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    for pair in sorted_pairs:
        print_template = ""
        for insn in range(len(pair[0])):
            print_template += pair[0][insn] + ", "
        print(f'{print_template:<64} {str(pair[1])}')


def main():
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    all_patterns_dict = {}

    for i in range(3, 8):
        all_patterns_dict.update(track_patterns(instr_trace, i))

    # Only printing the top third most frequent patterns to filter out the many patterns with a counter of 1

    # print(all_patterns_dict.items())
    # List comprehension to filter out patterns smaller than a certain counter value
    filtered_patterns = {k:r for k, r in all_patterns_dict.items() if r > 5}
    sorted_patterns = sorted(filtered_patterns.items(), key=lambda x: x[1], reverse=True)
    print_pairs(sorted_patterns)

if __name__ == "__main__":
    main()