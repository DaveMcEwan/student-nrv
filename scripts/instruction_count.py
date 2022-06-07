# Extract instructions from tracelog generated from Spike.
# Output the frequency of instructions used. 
import sys
import collections

def count_instructions():
    num_lines = 0
    for line in sys.stdin:
        num_lines += 1

    return num_lines

def main():
    print("All instructions : " + str(count_instructions()))

if __name__ == "__main__":
    main()
