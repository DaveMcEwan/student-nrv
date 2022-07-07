# Analyse the instruction trace input through stdin
# Measure how frequently specific registers are accessed

# Input : Trimmed down instruction trace
# Output : - JSON file containing the lists and dictionaries needed to make the display graphs from
#          - Formatted lists containing the counters associated with each register

# Example to guide use:
# Run the command : python3 scripts/reg_accesses/reg_accesses.py < scripts/example.trc
#   while in the base directory

import sys
import argparse
import csv
import logging
import json

# Print debugging information
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# Dont print debugging information
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
# Example debug printing line
# logging.debug("Test debugging")

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("--filedump", help="Filepath/name for the dictionary files")
args = parser.parse_args() # ISA argument stored in args.isa

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

# Function to take in the reg lists and form the desired dictionary format
def convert_reg(isa_part):
    dict_base = {}
    with open("isa/reg/rv32i.reg", 'r') as reg_file:
        for line in reg_file:
            sub_dict = dict_base[line.strip()] = {}
            sub_dict["rs"] = sub_dict["rd"] = 0

    return dict_base

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

# Iterate through the instruction trace and measure the frequency at which
#   registers are accessed
def track_regs(instr_trace, all_instrs, all_regs):
    # Initialise variables and dictionaries
    rs_dict = {}
    rd_dict = {}
    imm_dict = {}
    
    # Dictionary storing regular offsets such as those of loads and stores
    offset_dict = {}
    # Dictionary storing the offsets of jumps and branches
    branch_offset_dict = {}
    # Dictionary storing the shift sizes
    shift_dict = {}
    # Dictionary storing the values used for arithmetic
    arith_dict = {}

    counter = 0
    # Parse lines on stdin
    for line in instr_trace:
        counter += 1
        line_list = line.split()
        insn_name = line_list[2]

        # Check for instruction in overall dictionary
        if insn_name in all_instrs:
            logging.debug("")
            logging.debug(str(counter) + ": " + str(line_list[2:]))
            # Check what the register operand format is and assign variables accordingly
            insn_subdict = all_instrs[insn_name]
            if insn_subdict["Format"] == "R":
                # rd, rs1, rs2
                logging.debug("R Format")
                rd, rs1, rs2 = line_list[3:5]
                logging.debug("rd="+rd+", rs1="+rs1+", rs2="+rs2)

                # append_to_counter_dict(rd_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rd"] += 1
                # append_to_counter_dict(rs_dict, line_list[4][:-1])
                all_regs[line_list[4][:-1]]["rs"] += 1
                # append_to_counter_dict(rs_dict, line_list[5])
                all_regs[line_list[5]]["rs"] += 1
            elif insn_subdict["Format"] == "I":
                # rd, imm(rs)
                logging.debug("I Format")
                # append_to_counter_dict(rd_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rd"] += 1
                # Parse the second part of the assembly register format
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                # Not converting immediates to ints as we may get immediates as hex values
                append_to_counter_dict(imm_dict, remaining_string[0])
                # append_to_counter_dict(rs_dict, remaining_string[1])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rd="+line_list[3][:-1]+", imm="+remaining_string[0]+", rs="+remaining_string[1])
                # If this instruction is a shift instruction, increase it's corresponding 
                #   counter in the shift dictionary
                if (insn_subdict["Type"] == "shift"):
                    logging.debug("Shift detected")
                    append_to_counter_dict(shift_dict, remaining_string[0])
                elif(insn_subdict["Type"] == "load"):
                    logging.debug("Load detected")
                    append_to_counter_dict(offset_dict, remaining_string[0])
                elif(insn_subdict["Type"] == "arith"):
                    logging.debug("Arithmetic detected")
                    append_to_counter_dict(arith_dict, remaining_string[0])
            elif insn_subdict["Format"] == "S":
                # rs1, imm(rs2)
                logging.debug("S Format")

                # append_to_counter_dict(rs_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rs"] += 1
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                append_to_counter_dict(offset_dict, remaining_string[0])
                # append_to_counter_dict(rs_dict, remaining_string[1])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rs1="+line_list[3][:-1]+", imm/offset="+remaining_string[0]+", rs2="+remaining_string[1])
            elif insn_subdict["Format"] == "U":
                # rd, imm
                logging.debug("U Format")

                # append_to_counter_dict(rd_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rd"] += 1
                append_to_counter_dict(imm_dict, line_list[4])

                logging.debug("rd="+line_list[3][:-1]+", imm="+line_list[4])

                if(insn_subdict["Type"] == "arith"):
                    logging.debug("Arithmetic detected")
                    append_to_counter_dict(arith_dict, line_list[4])
                
            elif insn_subdict["Format"] == "SB":
                # rs1, rs2, pc + imm
                logging.debug("SB Format")

                # append_to_counter_dict(rs_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rs"] += 1
                # append_to_counter_dict(rs_dict, line_list[4][:-1])
                all_regs[line_list[4][:-1]]["rs"] += 1
                append_to_counter_dict(imm_dict, line_list[6]+line_list[7])
                append_to_counter_dict(branch_offset_dict, line_list[6]+line_list[7])

                logging.debug("rs1="+line_list[3][:-1]+ ", rs2="+line_list[4][:-1]+", imm/branch offset="+line_list[6]+line_list[7])

            elif insn_subdict["Format"] == "UJ":
                # pc + imm
                logging.debug("UJ Format")
                # append_to_counter_dict(rd_dict, "ra") # Return Address register
                all_regs["ra"]["rd"] += 1
                append_to_counter_dict(imm_dict, line_list[4]+line_list[5])
                append_to_counter_dict(branch_offset_dict, line_list[4]+line_list[5])

                logging.debug("rd=ra, imm/branch offset="+line_list[4]+line_list[5])

            elif insn_subdict["Format"] == "CR":     # Compressed formats
                # rs/d, rs
                logging.debug("CR Format")

                if(insn_name=="c.jr" or insn_name=="c.jalr"):
                    # rs
                    # append_to_counter_dict(rs_dict, line_list[3])
                    all_regs[line_list[3]]["rs"] += 1
                    logging.debug("rs="+line_list[3])
                    continue

                first_reg = line_list[3][:-1]
                # append_to_counter_dict(rd_dict, first_reg)
                all_regs[first_reg]["rd"] += 1
                # append_to_counter_dict(rs_dict, line_list[4])
                all_regs[line_list[4]]["rs"] += 1

                logging.debug("rd="+first_reg+", rs="+line_list[4])

                # Cases where the destination register is also being read from
                if(insn_name=="c.add" or insn_name=="c.addw" or insn_name=="c.sub"):
                    # append_to_counter_dict(rs_dict, first_reg)
                    all_regs[first_reg]["rs"] += 1
                    logging.debug("rs="+first_reg)

            elif insn_subdict["Format"] == "CI":
                # rs/d, imm,
                logging.debug("CI Format")

                first_reg = line_list[3][:-1]
                # append_to_counter_dict(rd_dict, first_reg)
                all_regs[first_reg]["rd"] += 1

                if(insn_subdict["Type"] == "load"):
                    # rd, imm(rs)
                    remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                    append_to_counter_dict(imm_dict, remaining_string[0])
                    append_to_counter_dict(offset_dict, remaining_string[0])
                    # append_to_counter_dict(rs_dict, remaining_string[1])
                    all_regs[remaining_string[1]]["rs"] += 1
                    logging.debug("rd="+first_reg + ", imm="+remaining_string[0] + ", rs="+remaining_string[1])
                    continue
                elif(insn_subdict["Type"] == "arith"):
                    logging.debug("Arithmetic detected")
                    append_to_counter_dict(arith_dict, line_list[4])

                append_to_counter_dict(imm_dict, line_list[4])

                logging.debug("rd="+first_reg+ ", imm="+line_list[4])

                # Cases where the dest register is also read from
                if(insn_name == "c.addi" or insn_name == "c.addiw" or 
                    insn_name == "c.addi16sp" or insn_name == "c.slli"):
                    # append_to_counter_dict(rs_dict, first_reg)
                    all_regs[first_reg]["rs"] += 1
                    logging.debug("rs="+first_reg)

            elif insn_subdict["Format"] == "CSS":
                # rs, imm(sp)
                logging.debug("CSS Format")

                # append_to_counter_dict(rs_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rs"] += 1

                offset = line_list[4].split("(")[0]
                append_to_counter_dict(imm_dict, offset)
                append_to_counter_dict(offset_dict, offset)
                # append_to_counter_dict(rs_dict, "sp")
                all_regs["sp"]["rs"] += 1

                logging.debug("rs1="+line_list[3][:-1]+", imm/offset="+line_list[4].split("(")[0]+", rs2=sp")

            elif insn_subdict["Format"] == "CIW":
                # rd, sp, imm
                logging.debug("CIW Format")

                # append_to_counter_dict(rd_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rd"] += 1
                # append_to_counter_dict(rs_dict, "sp")
                all_regs["sp"]["rs"] += 1
                append_to_counter_dict(imm_dict, line_list[5])
                append_to_counter_dict(arith_dict, line_list[5])

                logging.debug("rd="+line_list[3][:-1]+", rs=sp, "+", imm/arith="+line_list[5])

            elif insn_subdict["Format"] == "CL":
                # rd, imm(rs) - can merge with  'I'
                logging.debug("CL Format")

                # append_to_counter_dict(rd_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rd"] += 1
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                # append_to_counter_dict(rs_dict, remaining_string[1])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rd="+line_list[3][:-1]+", imm="+remaining_string[0]+", rs="+remaining_string[1])

            elif insn_subdict["Format"] == "CS":
                # rs1, imm(rs2) - can merge with 'S'
                logging.debug("CS Format")

                # append_to_counter_dict(rs_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rs"] += 1
                remaining_string = line_list[4].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                # append_to_counter_dict(rs_dict, remaining_string[1])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rs1="+line_list[3][:-1]+", imm="+remaining_string[0]+", rs2="+remaining_string[1])

            elif insn_subdict["Format"] == "CA":
                pass # TODO
            elif insn_subdict["Format"] == "CB":
                # rs, pc + imm
                logging.debug("CB Format")
                # append_to_counter_dict(rs_dict, line_list[3][:-1])
                all_regs[line_list[3][:-1]]["rs"] += 1
                append_to_counter_dict(imm_dict, line_list[6])

                logging.debug("rs="+line_list[3][:-1], "imm="+line_list[6])
            elif insn_subdict["Format"] == "CJ":
                # pc + imm
                logging.debug("CJ Format")
                # TODO : Add specific case for 'jumpl' instruction types where
                #   the return address is added to the rd dictionary
                if(insn_name=="c.jal"):
                    # append_to_counter_dict(rd_dict, "ra") # Return Address register
                    all_regs["ra"]["rd"] += 1
                append_to_counter_dict(imm_dict, line_list[4]+line_list[5])

                logging.debug("rd=ra"+", imm="+line_list[4]+line_list[5])
            else:
                pass # Do nothing if the column has nothing
    
    # Sort the lists
    sorted_rs = sorted(rs_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_rd = sorted(rd_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_imm = sorted(imm_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_offset = sorted(offset_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_branch_offset = sorted(branch_offset_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_shift = sorted(shift_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_arith = sorted(arith_dict.items(), key=lambda x: x[1], reverse=True)

    # Form the dictionary that will be passed onto the display script
    result = {}
    result["rs"] = sorted_rs
    result["rd"] = sorted_rd
    result["imm"] = sorted_imm
    result["offset_dict"] = sorted_offset
    result["branch_offset"] = sorted_branch_offset
    result["shift_dict"] = sorted_shift
    result["arith_dict"] = sorted_arith
    result["all_regs"] = all_regs

    with open('scripts/reg_accesses/test-rs.txt', 'w') as dump:
        dump.write(json.dumps(result))

    # Formatted printing so that users can access the raw data
    print("Most common source registers accessed: "
            +', '.join('[{}: {}]'.format(*k) for k in sorted_rs))
    print("Most common destination registers accessed: "
            +', '.join('[{}: {}]'.format(*k) for k in sorted_rd))
    print("Most common immediate values: "
            +', '.join('[{}: {}]'.format(*k) for k in sorted_imm))
    print("Most common address offsets: "
            +', '.join('[{}: {}]'.format(*k) for k in sorted_offset))
    print("Most common branch offsets: "
            +', '.join('[{}: {}]'.format(*k) for k in sorted_branch_offset))
    print("Most common shift sizes: "
            +', '.join('[{}: {}]'.format(*k) for k in shift_dict))
    print("Most common arithmetic immediates: "
            +', '.join('[{}: {}]'.format(*k) for k in sorted_arith))
    
    return all_regs

def main():
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    reg_dict = track_regs(instr_trace, check_isa(args.isa), convert_reg("t"))
    print(reg_dict)

if __name__ == "__main__":
    main()