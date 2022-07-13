# Identifying the most common sequences (in the form of pairs) where 
#   registers are read from (rs) or written to (rd)

# Input : Trimmed down instruction trace
# Output : TODO

# Example to guide use:
# Run the command : python3 scripts/reg_patterns/reg_only_pairs.py < scripts/example.trc
#   while in the base directory

import sys
import csv
import argparse

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # ISA argument stored in args.isa

# https://www.geeksforgeeks.org/python-import-from-parent-directory/
# Path adjusting to be able to append helper functions from scripts/
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import helper as hlp

# Function to take in a CSV file and convert it into the desired dictionary format
def convert_isa(isa_part):
    test_dict = {}
    with open("isa/"+isa_part+".isa", 'r') as data_file:
        data = csv.DictReader(filter(lambda row: row[0]!='#', data_file), skipinitialspace=True, delimiter=',')
        for row in data:
            # Initialise subdirectory
            sub_dict = test_dict.get(row["Insn"], dict())
            # Also want to include information on the instruction type
            #   to understand what the immediate is actually being used for
            sub_dict["Type"] = row["Type"]
            sub_dict["Format"] = row["Format"]

            test_dict[row["Insn"]] = sub_dict

    return test_dict

# Take in the input string detailing the ISA, parse it and grab the needed dictionaries
def check_isa(isa):
    all_instrs = {}

    # Determine base instruction set based on the XLEN
    if int(isa[2:4]) == 32:
        all_instrs.update(convert_isa("rv32"))
    else:
        # No file yet made for this condition
        all_instrs.update(convert_isa("rv64"))
    
    # Include relevant instructions based on the remaining instructions
    for index in range(5, len(isa)):
        all_instrs.update(convert_isa(isa[index]))
    # TODO : Consider extensions such as the bit manip ones which won't be 
    #   represented by just single characters; also need to consider
    #   CSV files which are combinations of extensions

    return all_instrs

# Helper function that checks if an item is in the input dictionary and increments
#   if it is or creates a key if it doesn't exist
def append_to_counter_dict(dict, insn_name):
    if(insn_name in dict):
        dict[insn_name] += 1
    else:
        dict[insn_name] = 1

# Measure the most frequent instruction pairs where there is an rs
def track_insn_rs_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    counter = 0
    while not key_string:
        line = instr_trace[counter].split()
        insn = line[2]
        rs1, rs2, _ = hlp.parse_instruction(line[2:], all_instrs)

        if rs1:
            key_string = insn + " " + rs1
            if rs2:
                key_string += " " + rs2 + ", "
            else:
                key_string += ", "        
        counter += 1

    for line in instr_trace[counter:]:
        line_list = line.split()
        insn = line_list[2]
        rs1, rs2, _ = hlp.parse_instruction(line_list[2:], all_instrs)

        # ---- If we want instructions without an rs to NOT BREAK patterns ---- #
        # if rs1:
        #     s_append = insn + " rs1:" + rs1
        #     if rs2:
        #         s_append += " rs2:" + rs2
        #     append_to_counter_dict(pairs_dict, key_string+s_append)
        #     key_string = s_append + ", "
        
        # ---- If we want instructions without an rs to BREAK patterns ---- #
        if rs1:
            if key_string: # Non-empty string
                s_append = insn + " rs1:" + rs1
                if rs2:
                    s_append += " rs2:" + rs2
                append_to_counter_dict(pairs_dict, key_string+s_append)

                # Prepare string for next pairing
                key_string = s_append + ", "
            else:  # Empty string
                key_string = insn + " rs1:" + rs1
                if rs2:
                    key_string += " rs2:" + rs2
                key_string += ", "
        else:
            key_string = ""

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Measure the most frequent instruction pairs where there is an rd
def track_insn_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    counter = 0
    while not key_string:
        line = instr_trace[counter].split()
        insn = line[2]
        _, _, rd = hlp.parse_instruction(line[2:], all_instrs)

        if rd:
            key_string = insn + " rd:" + rd + ", "
        
        counter += 1

    for line in instr_trace[counter:]:
        line_list = line.split()
        insn = line_list[2]
        _, _, rd = hlp.parse_instruction(line_list[2:], all_instrs)

        # ---- If we want instructions without an rd to NOT BREAK patterns ---- #
        # if rd:
        #     s_append = insn + " rd:" + rd
        #     append_to_counter_dict(pairs_dict, key_string+s_append)
        #     key_string = s_append + ", "
        
        # ---- If we want instructions without an rd to BREAK patterns ---- #
        if rd:
            s_append = insn + " rd:" + rd
            if key_string:
                append_to_counter_dict(pairs_dict, key_string+s_append)
            
            key_string  = s_append + ", "
        else:
            key_string = ""
        

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Measure the most frequent instruction pairs where there is either an rs or rd
def track_insn_rs_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    counter = 0
    while not key_string:
        line = instr_trace[counter].split()
        insn = line[2]
        rs1, rs2, rd = hlp.parse_instruction(line[2:], all_instrs)

        if rs1:
            key_string = insn + " rs1:" + rs1
            if rs2:
                key_string += " rs2:" + rs2
        
        if rd:
            if key_string:
                key_string += " rd:" + rd
            else:
                key_string = insn + " rd:" + rd
        
        if key_string:
            key_string += ", "

        counter += 1

    for line in instr_trace[counter:]:
        line_list = line.split()
        insn = line_list[2]
        rs1, rs2, rd = hlp.parse_instruction(line_list[2:], all_instrs)

        # ---- If we want instructions without an rs/rd to NOT BREAK patterns ---- #
        # s_append = ""
        # if rs1:
        #     s_append += insn + " rs1:" + rs1
        #     if rs2:
        #         s_append += " rs2:" + rs2

        # if rd:
        #     if s_append:
        #         s_append += " rd:" + rd
        #     else:
        #         s_append = insn + " rd:" + rd
        
        # if s_append:
        #     append_to_counter_dict(pairs_dict, key_string+s_append)
        #     key_string = s_append

        # ---- If we want instructions without an rs/rd to BREAK patterns ---- #
        # Must account for key_string potentially being empty

        empty = False if key_string else True

        s_append = ""
        if rs1:
            s_append += insn + " rs1:" + rs1
            if rs2:
                s_append += " rs2:" + rs2

        if rd:
            if not s_append:
                s_append += insn

            s_append += " rd:" + rd
        
        if s_append:
            if not empty:
                append_to_counter_dict(pairs_dict, key_string+s_append)
            key_string = s_append + ", "
        else:
            key_string = ""

        # ---- If we want instructions without an rs to BE INCLUDED IN patterns ---- #
        # Requires a separate function since the initialisation is different
        #   See track_all_insn_pairs()

    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Function used to track the most frequent instruction + (registers) patterns regardless
#   on whether or not there are registers associated with that instruction
def track_all_insn_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    key_string = ""

    # Initialise with the first instruction only
    line = instr_trace[0].split()
    insn = line[2]
    rs1, rs2, rd = hlp.parse_instruction(line[2:], all_instrs)

    key_string = insn
    if rs1:
        key_string += " rs1:" + rs1
        if rs2:
            key_string += " rs2:" + rs2
        
    if rd:
        key_string += " rd:" + rd
    
    key_string += ", "

    for line in instr_trace[1:]:
        line_list = line.split()
        insn = line_list[2]
        rs1, rs2, rd = hlp.parse_instruction(line_list[2:], all_instrs)

        s_append = insn
        if rs1:
            s_append += " rs1:" + rs1
            if rs2:
                s_append += " rs2:" + rs2

        if rd:
            s_append += " rd:" + rd
        
        append_to_counter_dict(pairs_dict, key_string+s_append)
        key_string = s_append + ", "
    
    return sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)

# Takes in the list of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    print("Printing pairs")
    for pair in sorted_pairs:
        print(f'{f"{pair[0]}":<32} {str(pair[1])}')

def main():
    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()

    print_pairs(track_all_insn_pairs(instr_trace, all_instrs))

if __name__ == "__main__":
    main()