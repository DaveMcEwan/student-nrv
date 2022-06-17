# Script used to calculate the moving average of a byte stream and plot the 
#   

import sys
import argparse
import matplotlib.pyplot as plt

import time
import numpy as np
import scipy
from scipy.ndimage.filters import uniform_filter1d

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Save path for the png figure")
args = parser.parse_args() # File path stored in args.img

def moving_average_scipy(input_stream, window_size):
    return list(scipy.convolve(input_stream, np.ones(window_size), 'same') / window_size)

def moving_average_numpy(input_stream, window_size):
    return list(np.convolve(input_stream, np.ones(window_size), 'same') / window_size)

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
    # input = map(str.rstrip, sys.stdin.readlines())
    input = sys.stdin.readlines()
    input_floats = [float(x) for x in input]

    start_numpy = time.time()
    print("Numpy convolve output:")
    print(moving_average_numpy(input_floats, 4))

    end = time.time()
    print("Scipy convolve output:")
    print(moving_average_scipy(input_floats, 4))
    end_scipy = time.time()

    print("Time taken to complete Numpy convolution: "+str(end-start_numpy))
    print("Time taken to complete Scipy convolution: "+str(end_scipy-end))

    # for n in range(10):
    #     n = 1 << n # Square the 2 to adjust the window size
    #     print("Window Size: "+str(n))

    #     print("Numpy Convolve : ")
    #     print(moving_average_numpy(input_floats, n))
    #     print("My Convolve: ")
    #     print(moving_average(input, n))
    #     print()

        # display_graph(moving_average(input, n), n)

if __name__ == "__main__":
    main()