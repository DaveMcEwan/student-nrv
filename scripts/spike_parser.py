# Extract instructions from tracelog generated from Spike.
# Output the frequency of instructions used. 
# Create bar chart and pie chart
import sys
import collections

def extract_instructions():

    # Category tests
    cat_all_loads = [ "c.lwsp", "c.lw", "lb", "lh", "lw", "lbu", "lhu", "flw", "c.flw", "c.flwsp" ] # No load immediate instructions because they don't access memory?
    cat_all_stores = [ "c.sw", "c.swsp", "sb", "sh", "sw", "c.fsw", "c.fswsp", "fsw" ]
    # Ints storing the number of load and store instructions that have been executed
    count_all_instrns = count_all_loads = count_all_stores = 0

    exception_found = False
    instructs = []

    for line in sys.stdin:
        words = line.split()
        if (words[2] != "exception" and not(exception_found)): # Instruction detected
            count_all_instrns += 1 # Increment instruction count
            # words[4] is the detected instruction

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

    print("All instructions : " + str(count_all_instrns))
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
