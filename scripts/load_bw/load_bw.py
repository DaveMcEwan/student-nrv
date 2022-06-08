# Analyse the instruction trace input through stdin
# Output the number of bytes transferred per instruction on the corresponding line
# Prepares the byte stream to then be used in the display script
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'isa'))

# These will have to be automated in the combined .isa files
loads_dict = {} # List of all dictionaries

import base_loads
print(base_loads.all_dicts)
loads_dict.update(base_loads.all_dicts)

import c_loads
print(c_loads.all_dicts)
loads_dict.update(c_loads.all_dicts)

def count_loads():
    for line in sys.stdin:
        words = line.split()
        if words[1] in loads_dict:
            print(loads_dict[words[1]]['bytes'])
        else:
            print(0)

def main():
    count_loads()

if __name__ == "__main__":
    main()
