import sys
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Save path for the png figure")
args = parser.parse_args() # File path stored in args.img

def moving_average(window_size):
    avg_stream = []
    window = []
    for bytes in map(str.rstrip, sys.stdin):
        window.append(int(bytes))
        if (len(window)) > window_size:
            window.pop(0)
        averaged_value = sum(window)/len(window)
        avg_stream.append(averaged_value)
        print(averaged_value)
    return avg_stream

def display_graph(avg_stream):
    time_axis = list(range(len(avg_stream)))
    plt.plot(time_axis, avg_stream)
    plt.title('Moving Average output')
    plt.xlabel('Line Number')
    plt.ylabel('Bytes transferred')
    plt.savefig(args.img)

def main():
    n = 128
    display_graph(moving_average(n))

if __name__ == "__main__":
    main()