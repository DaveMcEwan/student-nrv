# Analyse the instruction trace input through stdin
# Output the number of bytes transferred per load instruction 
#   on the corresponding line
# Prepares the byte stream to then be used in the display script

import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'isa'))

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")

args = parser.parse_args() # ISA stored in args.isa

# Import files/dictionaries based on the ISA argument
isa_dicts = __import__(args.isa)
# Overall dictionary for all instructions in this ISA is stored in :
#   isa_dicts.all_dicts

def count_loads():
    for line in sys.stdin:
        words = line.split()
        if words[1] in isa_dicts.load_dict:
            print(isa_dicts.load_dict[words[1]]['bytes'])
        else:
            print(0)

def main():
    count_loads()

if __name__ == "__main__":
    main()
