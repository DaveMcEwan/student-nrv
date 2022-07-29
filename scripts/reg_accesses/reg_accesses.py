# Analyse the instruction trace input through stdin
# Measure how frequently specific registers are accessed

# Input : Trimmed down instruction trace
# Output : - JSON file containing the lists and dictionaries needed to make the display graphs from
#          - Formatted lists containing the counters associated with each register

# Example to guide use:
# Run the command : python3 scripts/reg_accesses/reg_accesses.py \
#   --isa=rv32ic < scripts/example.trc
#   while in the base directory

import sys
import argparse
import logging
import json
import os

# Print debugging information
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# Dont print debugging information
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
# Example debug printing line
# logging.debug("Test debugging")

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common.isa_management import check_isa

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("--jsondump", help="Filepath/name for the JSON files")
args = parser.parse_args() # ISA argument stored in args.isa

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
    # Dictionary storing all immediate values and how often they are used
    imm_dict = {}
    # Dictionary storing regular offsets such as those of loads and stores
    address_offset_dict = {}
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
        insn_name = line_list[4]

        # Check for instruction in overall dictionary
        if insn_name in all_instrs:
            logging.debug("")
            logging.debug(str(counter) + ": " + str(line_list[4:]))
            # Check what the register operand format is and assign variables accordingly
            insn_subdict = all_instrs[insn_name]
            if insn_subdict["Format"] == "R":
                # rd, rs1, rs2
                logging.debug("R Format")
                rd, rs1, rs2 = line_list[5:7]
                logging.debug("rd="+rd+", rs1="+rs1+", rs2="+rs2)

                all_regs[line_list[5][:-1]]["rd"] += 1
                all_regs[line_list[6][:-1]]["rs"] += 1
                all_regs[line_list[7]]["rs"] += 1
            elif insn_subdict["Format"] == "I":
                # rd, imm(rs)
                logging.debug("I Format")
                all_regs[line_list[5][:-1]]["rd"] += 1
                # Parse the second part of the assembly register format
                remaining_string = line_list[6].replace("(", " ", 1)[:-1].split()
                # Not converting immediates to ints as we may get immediates as hex values
                append_to_counter_dict(imm_dict, remaining_string[0])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rd="+line_list[5][:-1]+", imm="+remaining_string[0]+", rs="+remaining_string[1])
                # If this instruction is a shift instruction, increase it's corresponding 
                #   counter in the shift dictionary
                if (insn_subdict["Type"] == "shift"):
                    logging.debug("Shift detected")
                    append_to_counter_dict(shift_dict, remaining_string[0])
                elif(insn_subdict["Type"] == "load"):
                    logging.debug("Load detected")
                    append_to_counter_dict(address_offset_dict, remaining_string[0])
                elif(insn_subdict["Type"] == "arith"):
                    logging.debug("Arithmetic detected")
                    append_to_counter_dict(arith_dict, remaining_string[0])
            elif insn_subdict["Format"] == "S":
                # rs1, imm(rs2)
                logging.debug("S Format")

                # append_to_counter_dict(rs_dict, line_list[5][:-1])
                all_regs[line_list[5][:-1]]["rs"] += 1
                remaining_string = line_list[6].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                append_to_counter_dict(address_offset_dict, remaining_string[0])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rs1="+line_list[5][:-1]+", imm/offset="+remaining_string[0]+", rs2="+remaining_string[1])
            elif insn_subdict["Format"] == "U":
                # rd, imm
                logging.debug("U Format")

                all_regs[line_list[5][:-1]]["rd"] += 1
                append_to_counter_dict(imm_dict, line_list[6])

                logging.debug("rd="+line_list[5][:-1]+", imm="+line_list[6])
                if(insn_subdict["Type"] == "arith"):
                    logging.debug("Arithmetic detected")
                    append_to_counter_dict(arith_dict, line_list[6])
                
            elif insn_subdict["Format"] == "SB":
                # rs1, rs2, pc + imm
                logging.debug("SB Format")

                all_regs[line_list[5][:-1]]["rs"] += 1
                all_regs[line_list[6][:-1]]["rs"] += 1
                append_to_counter_dict(imm_dict, line_list[8]+line_list[9])
                append_to_counter_dict(branch_offset_dict, line_list[8]+line_list[9])

                logging.debug("rs1="+line_list[5][:-1]+ ", rs2="+line_list[6][:-1]+", imm/branch offset="+line_list[8]+line_list[9])

            elif insn_subdict["Format"] == "UJ":
                # pc + imm
                logging.debug("UJ Format")
                all_regs["ra"]["rd"] += 1
                append_to_counter_dict(imm_dict, line_list[6]+line_list[7])
                append_to_counter_dict(branch_offset_dict, line_list[6]+line_list[7])

                logging.debug("rd=ra, imm/branch offset="+line_list[6]+line_list[7])

            elif insn_subdict["Format"] == "CR":     # Compressed formats
                # rs/d, rs
                logging.debug("CR Format")

                if(insn_name=="c.jr" or insn_name=="c.jalr"):
                    # rs
                    all_regs[line_list[5]]["rs"] += 1
                    logging.debug("rs="+line_list[5])
                    continue

                first_reg = line_list[5][:-1]
                all_regs[first_reg]["rd"] += 1
                all_regs[line_list[6]]["rs"] += 1

                logging.debug("rd="+first_reg+", rs="+line_list[6])

                # Cases where the destination register is also being read from
                if(insn_name=="c.add" or insn_name=="c.addw" or insn_name=="c.sub"):
                    all_regs[first_reg]["rs"] += 1
                    logging.debug("rs="+first_reg)

            elif insn_subdict["Format"] == "CI":
                # rs/d, imm,
                logging.debug("CI Format")

                first_reg = line_list[5][:-1]
                all_regs[first_reg]["rd"] += 1

                if(insn_subdict["Type"] == "load"):
                    # rd, imm(rs)
                    remaining_string = line_list[6].replace("(", " ", 1)[:-1].split()
                    append_to_counter_dict(imm_dict, remaining_string[0])
                    append_to_counter_dict(address_offset_dict, remaining_string[0])
                    all_regs[remaining_string[1]]["rs"] += 1
                    logging.debug("rd="+first_reg + ", imm="+remaining_string[0] + ", rs="+remaining_string[1])
                    continue
                elif(insn_subdict["Type"] == "arith"):
                    logging.debug("Arithmetic detected")
                    append_to_counter_dict(arith_dict, line_list[6])

                append_to_counter_dict(imm_dict, line_list[6])

                logging.debug("rd="+first_reg+ ", imm="+line_list[6])

                # Cases where the dest register is also read from
                if(insn_name == "c.addi" or insn_name == "c.addiw" or 
                    insn_name == "c.addi16sp" or insn_name == "c.slli"):
                    all_regs[first_reg]["rs"] += 1
                    logging.debug("rs="+first_reg)

            elif insn_subdict["Format"] == "CSS":
                # rs, imm(sp)
                logging.debug("CSS Format")

                all_regs[line_list[5][:-1]]["rs"] += 1

                offset = line_list[6].split("(")[0]
                append_to_counter_dict(imm_dict, offset)
                append_to_counter_dict(address_offset_dict, offset)
                all_regs["sp"]["rs"] += 1

                logging.debug("rs1="+line_list[5][:-1]+", imm/offset="+line_list[6].split("(")[0]+", rs2=sp")

            elif insn_subdict["Format"] == "CIW":
                # rd, sp, imm
                logging.debug("CIW Format")

                all_regs[line_list[5][:-1]]["rd"] += 1
                all_regs["sp"]["rs"] += 1
                append_to_counter_dict(imm_dict, line_list[7])
                append_to_counter_dict(arith_dict, line_list[7])

                logging.debug("rd="+line_list[5][:-1]+", rs=sp, "+", imm/arith="+line_list[7])

            elif insn_subdict["Format"] == "CL":
                # rd, imm(rs) - can merge with  'I'
                logging.debug("CL Format")

                all_regs[line_list[5][:-1]]["rd"] += 1
                remaining_string = line_list[6].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rd="+line_list[5][:-1]+", imm="+remaining_string[0]+", rs="+remaining_string[1])

            elif insn_subdict["Format"] == "CS":
                # rs1, imm(rs2) - can merge with 'S'
                logging.debug("CS Format")

                all_regs[line_list[5][:-1]]["rs"] += 1
                remaining_string = line_list[6].replace("(", " ", 1)[:-1].split()
                append_to_counter_dict(imm_dict, remaining_string[0])
                all_regs[remaining_string[1]]["rs"] += 1

                logging.debug("rs1="+line_list[5][:-1]+", imm="+remaining_string[0]+", rs2="+remaining_string[1])

            elif insn_subdict["Format"] == "CA":
                pass # TODO
            elif insn_subdict["Format"] == "CB":
                # rs, pc + imm
                logging.debug("CB Format")
                all_regs[line_list[5][:-1]]["rs"] += 1
                append_to_counter_dict(imm_dict, line_list[8])

                logging.debug("rs="+line_list[5][:-1], "imm="+line_list[8])
            elif insn_subdict["Format"] == "CJ":
                # pc + imm
                logging.debug("CJ Format")
                # TODO : Add specific case for 'jumpl' instruction types where
                #   the return address is added to the rd dictionary
                if(insn_name=="c.jal"):
                    all_regs["ra"]["rd"] += 1
                append_to_counter_dict(imm_dict, line_list[6]+line_list[7])

                logging.debug("rd=ra"+", imm="+line_list[6]+line_list[7])
            else:
                pass # Do nothing if the column has nothing
    
    # Sort the lists
    sorted_imm = sorted(imm_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_offset = sorted(address_offset_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_branch_offset = sorted(branch_offset_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_shift = sorted(shift_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_arith = sorted(arith_dict.items(), key=lambda x: x[1], reverse=True)

    # Form the dictionary that will be passed onto the display script
    result = {}
    result["imm"] = sorted_imm
    result["address_offset"] = sorted_offset
    result["branch_offset"] = sorted_branch_offset
    result["shift"] = sorted_shift
    result["arith"] = sorted_arith
    result["all_regs"] = all_regs

    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(result))

    # Formatted printing so that users can access the raw data
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
    
def main():
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    # Keys we want to access from the .isa files
    key_list = ["Type", "Format"]
    all_instrs, regs = check_isa(args.isa, key_list, reg=True)
    track_regs(instr_trace, all_instrs, regs)

if __name__ == "__main__":
    main()