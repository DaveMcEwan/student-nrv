# Analyse the instruction trace input through stdin
# Measure how frequently specific registers are accessed

# Input : Trimmed down instruction trace
# Output : - JSON file containing the dictionaries storing counters regarding
#   how often each register is used as what. Used to make the display graphs.

# Example to guide use:
# Run the command : python3 scripts/reg_accesses/reg_accesses.py \
#   --isa=rv32ic -j=<json dump> < scripts/example.trc
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
from common.reg_functions import parse_instruction

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("-j", "--jsondump", help="Filepath/name for the JSON files")
args = parser.parse_args() # ISA argument stored in args.isa

# Iterate through the instruction trace and measure the frequency at which
#   registers are accessed
def track_regs(instr_trace, all_instrs, all_regs):
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
            rs1, rs2, rd = parse_instruction(line_list[4:], all_instrs)
            if rs1:
                logging.debug("rs1: "+str(rs1))
                all_regs[rs1]["rs"] += 1
            if rs2:
                logging.debug("rs2: "+str(rs2))
                all_regs[rs2]["rs"] += 1
            if rd:
                logging.debug("rd: "+str(rd))
                all_regs[rd]["rd"] += 1
    
    if args.jsondump:
        with open(args.jsondump, 'w') as dump:
            dump.write(json.dumps(all_regs))
    
def main():
    # Read in the stdin and store in the instr_trace variable
    instr_trace = sys.stdin.readlines()
    # Keys we want to access from the .isa files
    key_list = ["Type", "Format"]
    all_instrs, regs = check_isa(args.isa, key_list, reg=True)
    track_regs(instr_trace, all_instrs, regs)

if __name__ == "__main__":
    main()