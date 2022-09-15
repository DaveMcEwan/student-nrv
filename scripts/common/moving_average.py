# Script used to only calculate the moving average of any stream of
#   values based on an input argument value that determines the window size

# Input : Raw byte stream 
#   e.g. scripts/bandwidth/load_bw/example-load-bytes.txt
# Output : 
#   - Average byte stream - Printed to stdout
#       e.g. scripts/bandwidth/load_bw/example-load-bytes-avg.txt

# Example to guide use:
# Run the command : python3 scripts/common/moving_average.py \
#       -n=4 \
#       < scripts/bandwidth/load_bw/example-load-bytes.txt \
#       > scripts/bandwidth/load_bw/example-load-bytes-avg.txt
#   while in the base directory

import sys
import argparse
import numpy as np
import json

# Script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--window", help="Moving Average window size")
parser.add_argument("-l", "--sizedump", help="Output file for the number of \
    instructions to facilitate processing in other scripts.")
args = parser.parse_args()

def main():
    # Initialise Numpy array window
    window_array = np.zeros([int(args.window)])

    # Counter used to determine how many lines there are
    counter = 0
    for value in sys.stdin:
        counter += 1
        window_array[0] = float(value)
        window_array = np.roll(window_array, -1)

        print(sum(window_array)/float(args.window))

    if args.sizedump:
        with open(args.sizedump, 'w') as dump:
            dump.write(json.dumps(counter))

if __name__ == "__main__":
    main()