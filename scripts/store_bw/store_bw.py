# Analyse the instruction trace input through stdin
# Output the number of bytes transferred per store instruction on the corresponding line
# Prepares the byte stream to then be used in the display script
import sys

# TODO : Add code to include dictionaries and lists from the associated .isa file.
#   Need a way of getting the configuration from the instruction trace - maybe
#   by looking at the instruction trace's parent directories

# These are examples dictionaries that may be included from the .isa file
base_loads = {  'sw': {'bytes': 4, 'cycles': 0}, 
                'sh': {'bytes': 2, 'cycles': 0},
                'sb': {'bytes': 1, 'cycles': 0},
             }

c_sp_loads = {  'c.swsp': {'bytes': 4, 'cycles': 0}, 
                'c.sdsp': {'bytes': 8, 'cycles': 0},
                'c.sqsp': {'bytes': 16, 'cycles': 0},
                'c.fswsp': {'bytes': 8, 'cycles': 0},
                'c.fsdsp': {'bytes': 16, 'cycles': 0},
             }

c_reg_loads = { 'c.sw': {'bytes': 4, 'cycles': 0}, 
                'c.sd': {'bytes': 8, 'cycles': 0},
                'c.sq': {'bytes': 16, 'cycles': 0},
                'c.fsw': {'bytes': 4, 'cycles': 0},
                'c.fsd': {'bytes': 8, 'cycles': 0},
              }

# These will have to be automated in the combined .isa files
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
