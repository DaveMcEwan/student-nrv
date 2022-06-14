import sys
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Save path for the png figure")
args = parser.parse_args() # File path stored in args.img

def moving_average(input_stream, window_size):
    avg_stream = []
    window = []
    for bytes in input_stream:
        # print("Bytes:"+bytes)
        window.append(int(bytes))
        if (len(window)) > window_size:
            window.pop(0)
        averaged_value = sum(window)/len(window)
        avg_stream.append(averaged_value)
        print(averaged_value)
    return avg_stream

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
    print(input)

    for n in range(10):
        n = 1 << n # Square the 2 to adjust the window size
        print("Window Size: "+str(n))
        display_graph(moving_average(input, n), n)

if __name__ == "__main__":
    main()