# Analyse the instruction trace input through stdin
# Output the number of bytes transferred per store instruction 
#   on the corresponding line
# Prepares the byte stream to then be used in the display script

# Input : Trimmed down instruction trace
# Output : Store byte stream (to then be passed through a moving average filter)
# --isa flag : Determines the instructions we expect to see in the program; same as
#   the --isa flag in Spike

# Example to guide use:
# Run the command : python3 scripts/store_bw/store_bw.py --isa=rv32ic < scripts/example.trc
#   while in the base directory

import sys
import argparse
import csv

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
args = parser.parse_args() # ISA argument stored in args.isa

# Function to take in a CSV file and convert it into the desired dictionary format
def convert_csv_to_dict_st_only(isa):
    test_dict = {}
    with open("isa/"+isa+".isa", 'r') as data_file:
        data = csv.DictReader(filter(lambda row: row[0]!='#', data_file), skipinitialspace=True, delimiter=',')
        for row in data:
            test_dict[row["Insn"]] = int(row["St"])

    return test_dict

# Take in the input string detailing the ISA, parse it and grab the needed dictionaries
def check_isa(isa):
    all_instrs = {}

    # Determine base instruction set based on the XLEN
    if int(isa[2:4]) == 32:
        all_instrs.update(convert_csv_to_dict_st_only("rv32"))
    else:
        # No file yet made for this condition
        all_instrs.update(convert_csv_to_dict_st_only("rv64"))
    
    # Include relevant instructions based on the remaining instructions
    for index in range(5, len(isa)):
        all_instrs.update(convert_csv_to_dict_st_only(isa[index]))
    # TODO : Consider extensions such as the bit manip ones which won't be 
    #   represented by just single characters; also need to consider
    #   CSV files which are combinations of extensions

    return all_instrs

#   Iterate through the instruction stream and output the byte stream
def count_stores(all_instrs):
    for line in sys.stdin:
        words = line.split()
        insn_name = words[1]

        if insn_name in all_instrs:
            print(all_instrs[insn_name])
        else:
            print(0)

def main():
    all_instrs = {}
    all_instrs = check_isa(args.isa)
    count_stores(all_instrs)

if __name__ == "__main__":
    main()
