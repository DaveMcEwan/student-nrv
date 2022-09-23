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
import math

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
    # TODO : Work on a way to have the Xticks be adjusted in size and quantity
    #   with respect to the figure size/how big the data is
    # plt.xticks(np.arange(0, avg_stream.size, \
    #     (min(round((avg_stream.size/50)/100)*100, 1300))))

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
    
    fig = plt.gcf()
    # TODO : Work on setting up a figure size that adjusts well to the size
    #   of the input data.
    fig.set_size_inches(min(avg_stream.size/100, 620.35), 5)
    fig.savefig(args.img)

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
    index = 0

    # Read data into NumPy array first then slice accordingly
    values[index] = sys.stdin.read(3)
    while index < (line_count - 1):
        index += 1
        values[index] = sys.stdin.read(3)

    max_size = 5000000
    if line_count > max_size: # Need to truncate and sample
        print("Original line count : "+str(line_count))
        slice_index = math.ceil(line_count / max_size)
        print("Slice index = "+str(slice_index))
        new_size = math.floor(line_count / slice_index) * slice_index
        print("New size : "+str(new_size))
        print(values[:new_size].size)
        display_graph(np.mean(values[:new_size].reshape(new_size/slice_index,slice_index), axis=1))
    else:
        display_graph(values)
    

if __name__ == "__main__":
    main()