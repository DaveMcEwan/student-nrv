# Extract instructions from tracelog generated from Spike.
# Output the frequency of instructions used. 
import sys
import collections

# TODO : Add code to include dictionaries and lists from the associated .isa file.
#   Need a way of getting the configuration from the instruction trace - maybe
#   by looking at the instruction trace's parent directories

# These are examples dictionaries that may be included from the .isa file
base_loads = {  'lw': {'bytes': 4, 'cycles': 0}, 
                'lh': {'bytes': 2, 'cycles': 0},
                'lhu': {'bytes': 2, 'cycles': 0},
                'lb': {'bytes': 1, 'cycles': 0},
                'lbu': {'bytes': 1, 'cycles': 0},
             }

c_sp_loads = {  'c.lwsp': {'bytes': 4, 'cycles': 0}, 
                'c.ldsp': {'bytes': 8, 'cycles': 0},
                'c.lqsp': {'bytes': 16, 'cycles': 0},
                'c.flwsp': {'bytes': 4, 'cycles': 0},
                'c.fldsp': {'bytes': 8, 'cycles': 0},
             }

c_reg_loads = { 'c.lw': {'bytes': 4, 'cycles': 0}, 
                'c.ld': {'bytes': 8, 'cycles': 0},
                'c.lq': {'bytes': 16, 'cycles': 0},
                'c.flw': {'bytes': 4, 'cycles': 0},
                'c.fld': {'bytes': 8, 'cycles': 0},
              }

# This will have to be automated in the combined .isa files
loads_list = []
loads_list.extend(base_loads.keys())
loads_list.extend(c_sp_loads.keys()) 
loads_list.extend(c_reg_loads.keys())

loads_dict = {}
loads_dict.update(base_loads)
loads_dict.update(c_sp_loads)
loads_dict.update(c_reg_loads)

def count_loads():
    for line in sys.stdin:
        words = line.split()
        if words[1] in loads_list:
            print(loads_dict[words[1]]['bytes'])
        else:
            print(0)

def main():
    count_loads()

if __name__ == "__main__":
    main()
