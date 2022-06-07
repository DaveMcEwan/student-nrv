# Extract instructions from tracelog generated from Spike.
# Output the frequency of instructions used. 
import sys
import collections

def count_mem_instructions():
    # Categories for load and store instructions; TODO : Build upon and make sure everything is included
    cat_all_loads = [ "c.lwsp", "c.lw", "lb", "lh", "lw", "lbu", "lhu", "flw", "c.flw", "c.flwsp" ] # No load immediate instructions because they don't access memory?
    cat_all_stores = [ "c.sw", "c.swsp", "sb", "sh", "sw", "c.fsw", "c.fswsp", "fsw" ]

    count_all_loads = count_all_stores = 0

    for line in sys.stdin:
        words = line.split()
        if words[1] in cat_all_loads:
            count_all_loads += 1
        elif words[1] in cat_all_stores:
            count_all_stores += 1

    print("Number of load instructions : " + str(count_all_loads))
    print("Number of store instructions : " + str(count_all_stores))

def main():
    count_mem_instructions()

if __name__ == "__main__":
    main()
