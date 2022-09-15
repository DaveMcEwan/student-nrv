# Script used to plot a line graph for an input stream of values

# Input : Average byte stream 
#   e.g. scripts/bandwidth/load_bw/example-load-bytes-avg.txt
# Output : 
#   - Figure - Saved in file path determined by the input argument for --img
#       e.g. scripts/bandwidth/load_bw/example-load-bytes.png

# Example to guide use:
# Run the command : python3 scripts/display/line_graph.py \
#       --img=scripts/bandwidth/load_bw/example-load-bytes.pdf \
#       -p=mov_avg \
#       -n=4 \
#       < scripts/bandwidth/load_bw/example-load-bytes-avg.txt
#   while in the base directory

import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

# Script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--sizedump", help="File with the counter detailing \
    how many lines to expect.")
parser.add_argument("-i", "--img", help="Save path for the pdf figure") # File path stored in args.img
parser.add_argument("-p", "--profile", help="Display profile, choose from: \
    mov_avg or leave empty for default title/axis names") # args.profile
parser.add_argument("-n", "--window", help="Moving Average window size") # args.window
args = parser.parse_args()

# Function to display the line graph
def display_graph(avg_stream):
    plt.plot(avg_stream)

    # Determine axis names based on the input profile
    # Add future profiles here
    if args.profile == "mov_avg":
        # Note that this requires a value for the --window argument
        plt.title("Moving Average output for n="+args.window)
        plt.ylabel("Bytes transferred")
    else:
        plt.title("Line graph")
        plt.ylabel("Magnitude")

    plt.xlabel('Line Number')
    plt.savefig(args.img)

def main():
    line_count = 0
    if args.sizedump:
        with open(args.sizedump, 'r') as dump:
            line_count = int(dump.readline())
    else:
        print("-l/--sizedump flag not specified. This must point to a file \
            which just contains the number of lines in the input stream")
        return 1
    
    values = np.empty([line_count])

    for num, line in enumerate(sys.stdin):
        values[num] = line

    display_graph(values)

if __name__ == "__main__":
    main()