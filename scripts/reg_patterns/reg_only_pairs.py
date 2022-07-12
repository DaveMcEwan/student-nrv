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

# Iterate through instruction trace and count the most frequent register access pairs
def track_rs_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    # String variable forming the base which we'll make the keys from
    key_string = ""

    counter = 0
    # Initialise key_string
    while not key_string:
        line = instr_trace[counter]
        rs1, rs2, _ = hlp.parse_instruction(line.split()[2:], all_instrs)

        if rs1:
            key_string = rs1 + ", "
            if rs2:
                key_string += rs2
                append_to_counter_dict(pairs_dict, key_string)
                key_string = rs2 + ", "

        counter += 1

    # key_string is guaranteed to have a reg already in it now
    for line in instr_trace[counter:]:
        rs1, rs2, _ = hlp.parse_instruction(line.split()[2:], all_instrs)
        # print("rs1 :"+rs1+", rs2:"+rs2)

        if rs1: # Variable present in rs1, append to pairing
            # print("rs1: "+rs1)
            key_string += rs1
            # print("Adding single: "+rs1)
            append_to_counter_dict(pairs_dict, key_string)
            # print("Adding: "+key_string)
            key_string = rs1+ ", "
            if rs2: # Check if rs2 is present (only if rs1 is present)
                # print("rs2: "+rs2)
                key_string += rs2
                # print("Adding single: "+rs2)
                append_to_counter_dict(pairs_dict, key_string)
                # print("Adding: "+key_string)
                key_string = rs2 + ", "
    
    # Sort based on the corresponding counter values
    sorted_pairs = sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_pairs

def track_rd_pairs(instr_trace, all_instrs):
    pairs_dict = {}
    # String variable forming the base which we'll make the keys from
    key_string = ""

    counter = 0
    # Initialise key_string
    while not key_string:
        line = instr_trace[counter]
        _, _, rd = hlp.parse_instruction(line.split()[2:], all_instrs)
        if rd:
            # print(rd)
            key_string += rd + ", "
        counter += 1

    # key_string is guaranteed to have a reg already in it now
    for line in instr_trace[counter:]:
        _, _, rd = hlp.parse_instruction(line.split()[2:], all_instrs)
        if rd:
            # print(rd)
            key_string += rd
            append_to_counter_dict(pairs_dict, key_string)
            key_string = rd+ ", "
    
    # Sort based on the corresponding counter values
    sorted_pairs = sorted(pairs_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_pairs

def track_rs_rd_pairs(instr_trace, all_instrs):
    rs_dict = {}
    rd_dict = {}
    # String variable forming the base which we'll make the keys from
    rs_string = ""
    rd_string = ""

    counter = 0
    # Initialise strings
    while not rs_string and not rd_string:
        line = instr_trace[counter]
        rs1, rs2, rd = hlp.parse_instruction(line.split()[2:], all_instrs)

        if rs1:
            if rs_string: # Already has a reg in it
                rs_string += rs1
                append_to_counter_dict(rs_dict, rs_string)
            rs_string = rs1 + ", "

            if rs2: # Guaranteed to already have a reg in rs_string beforehand
                rs_string += rs2
                append_to_counter_dict(rs_dict, rs_string)
                rs_string = rs2 + ", "

        if rd:
            if rd_string: # Already has a reg
                rd_string += rd
                append_to_counter_dict(rd_dict, rd_string)
            rd_string = rd + ", "
        counter += 1

    for line in instr_trace[counter:]:
        rs1, rs2, rd = hlp.parse_instruction(line.split()[2:], all_instrs)
        # print("rs1 :"+rs1+", rs2:"+rs2+", rd:"+rd)

        # TODO : Fix the rs_string checking to match the individual functions
        if rs1:
            # print("rs1: "+rs1)
            rs_string += rs1
            append_to_counter_dict(rs_dict, rs_string)
            rs_string = rs1 + ", "
            if rs2:
                # print("rs2: "+rs2)
                rs_string += rs2
                append_to_counter_dict(rs_dict, rs_string)
                rs_string = rs2 + ", "

        if rd:
            # print("rd: "+rd)
            rd_string += rd
            append_to_counter_dict(rd_dict, rd_string)
            rd_string = rd + ", "

    sorted_rs = sorted(rs_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_rd = sorted(rd_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_rs, sorted_rd

def track_rs_patterns(instr_trace, window_size, all_instrs):
    rs_pattern_dict = {}
    window = []

    for line in instr_trace:
        rs1, rs2, _ = hlp.parse_instruction(line.split()[2:], all_instrs)

        if rs1:
            # print("rs1: "+rs1)
            if len(window) == window_size: # If the window has been filled
                window.append(rs1)
                window = window[1:]
                append_to_counter_dict(rs_pattern_dict, tuple(window))
            elif len(window) == window_size - 1: # Window is 1 away from being filled
                window.append(rs1)
                append_to_counter_dict(rs_pattern_dict, tuple(window))
            else: # Window has not yet been filled
                window.append(rs1)
            if rs2:
                # print("rs2: "+rs2)
                if len(window) == window_size:
                    window.append(rs2)
                    window = window[1:]
                    append_to_counter_dict(rs_pattern_dict, tuple(window))
                elif len(window) == window_size - 1:
                    window.append(rs2)
                    append_to_counter_dict(rs_pattern_dict, tuple(window))
                else:
                    window.append(rs2)

    return sorted(rs_pattern_dict.items(), key=lambda x: x[1], reverse=True)

# Takes in the list of tuples and prints out the pairs and counters in a readable way
def print_pairs(sorted_pairs):
    print("Printing pairs")
    for pair in sorted_pairs:
        print(f'{f"{pair[0]}":<32} {str(pair[1])}')

def main():
    all_instrs = check_isa(args.isa)
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    # print("Most common RS pairs")
    # print_pairs(track_rs_pairs(instr_trace, all_instrs))
    # print("Most common RD pairs")
    # print_pairs(track_rd_pairs(instr_trace, all_instrs))

    rs_list, rd_list = track_rs_rd_pairs(instr_trace, all_instrs)
    # print("Most common RS pairs")
    # print_pairs(rs_list)
    # print("Most common RD pairs")
    # print_pairs(rd_list)

    print_pairs(track_rs_patterns(instr_trace, 5, all_instrs))

if __name__ == "__main__":
    main()