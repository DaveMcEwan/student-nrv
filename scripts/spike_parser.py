# Extract instructions from tracelog generated from Spike.
# Output the frequency of instructions used. 
# Create bar chart and pie chart
import sys
import collections

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

def extract_instructions():

    # Category tests
    cat_all_loads = [ "c.lwsp", "c.lw", "lb", "lh", "lw", "lbu", "lhu", "flw", "c.flw", "c.flwsp" ] # No load immediate instructions because they don't access memory?
    cat_all_stores = [ "c.sw", "c.swsp", "sb", "sh", "sw", "c.fsw", "c.fswsp", "fsw" ]
    # Ints storing the number of load and store instructions that have been executed
    count_instrns = count_cycles = count_all_loads = count_all_stores = 0

    exception_found = False
    instructs = []

    for line in sys.stdin:
        words = line.split()
        if (words[2] != "exception" and not(exception_found)): # Instruction detected
            count_instrns += 1 # Increment instruction count
            # words[4] is the detected instruction
            # Increase cycle count
            if words[4] not in cpi_list:
                count_cycles += 1
            else:
                count_cycles += cpi_list[words[4]]

            if words[4] in cat_all_loads:
                count_all_loads += 1
            elif words[4] in cat_all_stores:
                count_all_stores += 1
            instructs.append(words[4])

        elif (words[2] == "exception"):
            exception_found = True

        # Handles the tval instruction
        elif (len(words) < 5 and exception_found):  
            pass

        elif (exception_found):
            if (words[4] == "sret"):
                exception_found = False

    print("All instructions : " + str(count_instrns))
    print("Number of cycles : " + str(count_cycles))
    print("All loads : " + str(count_all_loads))
    print("All stores : " + str(count_all_stores))
    print("")
    return collections.Counter(instructs)

def print_results(freq_instructs):
    for op, count in freq_instructs.items():
        print(op + "," + str(count))


def main():
    freq_instructs = dict(extract_instructions())
    print_results(freq_instructs)

if __name__ == "__main__":
    main()
