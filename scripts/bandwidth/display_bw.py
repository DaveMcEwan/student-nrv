# Script used to calculate the moving average of a byte stream and plot 
#   a line graph for the input window size

# Input : Raw byte stream 
#   e.g. scripts/bandwidth/load_bw/example-load-bytes.txt
# Output : 
#   - Average byte stream - Printed to stdout
#       e.g. scripts/bandwidth/load_bw/example-load-bytes-avg.txt
#   - Figure - Saved in file path determined by the input argument for --img
#       e.g. scripts/bandwidth/load_bw/example-load-bytes.png

# Example to guide use:
# Run the command : python3 scripts/bandwidth/display_bw.py \
#       --img=scripts/bandwidth/load_bw/example-load-bytes.pdf \
#       -n=4 \
#       < scripts/bandwidth/load_bw/example-load-bytes.txt \
#       > scripts/bandwidth/load_bw/example-load-bytes-avg.txt
#   while in the base directory

import sys
import argparse
import matplotlib.pyplot as plt
import scipy

# Script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--img", help="Save path for the pdf figure") # File path stored in args.img
parser.add_argument("-n", "--window", help="Moving Average window size") # args.window
args = parser.parse_args()

# Moving average window function
def moving_average_scipy(input_stream):
    avg = scipy.convolve(input_stream, [1]*int(args.window), 'same') / int(args.window)
    print( "Byte stream trace, moving average window size = "+args.window)
    print(*avg, sep='\n') # Print each value on a new line
    return list(avg)

# Function to display the line graph
def display_graph(avg_stream):
    time_axis = list(range(len(avg_stream)))

    plt.plot(time_axis, avg_stream)
    plt.title('Moving Average output for n='+args.window)
    plt.xlabel('Line Number')
    plt.ylabel('Bytes transferred')
    plt.savefig(args.img)

def main():
    # Read the stdin input as a variable so we can then return to it
    input = sys.stdin.readlines()
    input_floats = [float(x) for x in input]

    display_graph(moving_average_scipy(input_floats))

if __name__ == "__main__":
    main()