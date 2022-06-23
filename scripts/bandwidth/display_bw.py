# Script used to calculate the moving average of a byte stream and plot 
#   several line graphs for different moving average window sizes

import sys
import argparse
import matplotlib.pyplot as plt

import scipy

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Save path for the png figure")
args = parser.parse_args() # File path stored in args.img

def moving_average_scipy(input_stream, window_size):
    return list(scipy.convolve(input_stream, [1]*window_size, 'same') / window_size)

def display_graph(avg_stream, n):
    time_axis = list(range(len(avg_stream)))

    plt.figure(n)
    plt.plot(time_axis, avg_stream)
    plt.title('Moving Average output for n='+str(n))
    plt.xlabel('Line Number')
    plt.ylabel('Bytes transferred')
    plt.savefig(args.img+"_"+str(n)+".png")

def main():
    # Read the stdin input as a variable so we can then return to it
    input = sys.stdin.readlines()
    input_floats = [float(x) for x in input]

    for n in range(10):
        n = 1 << n # Square the 2 to adjust the window size
        display_graph(moving_average_scipy(input_floats, n), n)

if __name__ == "__main__":
    main()