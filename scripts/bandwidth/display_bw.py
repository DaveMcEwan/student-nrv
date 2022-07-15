# Script used to calculate the moving average of a byte stream and plot 
#   several line graphs for different moving average window sizes

import sys
import argparse
import matplotlib.pyplot as plt

import scipy

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Save path for the pdf figure") # File path stored in args.img
parser.add_argument("-n", "--window", help="Moving Average window size") # args.window
args = parser.parse_args() 

def moving_average_scipy(input_stream):
    return list(scipy.convolve(input_stream, [1]*int(args.window), 'same') / int(args.window))

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