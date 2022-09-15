# Analyse the instruction trace input through stdin
# Look at the key passed in by the programmer through the --key flag and print
#   an output trace of each instruction's value associated with that key
#   to stdout.
# Used to output the bandwidth streams.

# Input : Instruction trace
# Output : Load byte stream (to then be passed through a moving average filter)
# --isa flag : Determines the instructions we expect to see in the program; same as
#   the --isa flag in Spike

# Example to guide use:
# Run the command : python3 scripts/common/key_stream.py --isa=rv32ic --key=Ld \
#                   < scripts/example.trc
#   while in the base directory

import sys
import argparse
import os

# Adding the parent directory to the python file path to 
#   allow absolute file path inclusions
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common.isa_management import check_isa

# Input argument parsing (to detect the ISA)
parser = argparse.ArgumentParser()
parser.add_argument("--isa", help="RISC-V ISA string")
parser.add_argument("-k", "--key", help="Key from the CSV values that we want to \
    access the values from and print in a stream")
args = parser.parse_args() # ISA argument stored in args.isa

#   Iterate through the instruction stream and output the byte stream
def print_key_stream(all_instrs):
    # print("Stream of values associated with the key: "+args.key)
    for line in sys.stdin:
        words = line.split()
        insn_name = words[4]

        if insn_name in all_instrs:
            print(all_instrs[insn_name])
        else:
            print(0) # TODO : Make sure this doesn't mess with other instruction traces
            #    other than bandwidth stuff

def main():
    print_key_stream(check_isa(args.isa, args.key))

if __name__ == "__main__":
    main()