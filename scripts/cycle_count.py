# Extract instructions from tracelog generated from Spike.
# Output the frequency of instructions used. 
import sys
import collections

# TODO : Expand CPI list and ensure that it is entirely correct rather than just taking Daniel's list
cpi_list = {
# Sign inject
        'fabs.s': 3,
        'fsgnj.s': 3,
        'fsgnjn.s': 3,
        'fsgnjx.s': 3,

# Arithmetic
        'fadd.s': 2,
        'fsub.s': 2,
        'remu': 6,
        'rem': 6,
        'divu': 6,
        'div': 6,
        'fdiv.s': 6,
        'fmul.s': 2,
        'fsqrt.s': 6,
        'fmadd.s': 2,
        'fmsub.s': 2,

# Negate arithmetic
        'fneg.s': 3,
        'fnmadd.s': 2,
        'fnmsub.s': 2,

# Compare
        'fmax.s': 3,
        'fmin.s': 3,
        
# Move
        'fmv.s': 3,

# Load Store
        'lh': 2,
        'lhu': 2,
        'lb': 2,
        'lbu': 2,
        'lw': 2,
        'c.lw': 2,
        'flw': 2,
        'fsw': 2,
        'c.flw': 2,
        'c.fsw': 2,
        'c.flwsp': 2
}

def count_cycles():
    num_cycles = 0
    for line in sys.stdin:
        words = line.split()
        if words[1] not in cpi_list:
            num_cycles += 1
        else:
            num_cycles += cpi_list[words[1]]

    return num_cycles


def main():
    print("Number of cycles : " + str(count_cycles()))

if __name__ == "__main__":
    main()
