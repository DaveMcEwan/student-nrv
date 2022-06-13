import sys
import matplotlib.pyplot as plt

def moving_average(window_size):
    avg_stream = []
    window = []
    for bytes in map(str.rstrip, sys.stdin):
        avg_stream.append(int(bytes))
        window.append(int(bytes))
        if (len(window)) > window_size:
            window.pop(0)
        print(sum(window)/len(window))
    return avg_stream

def display_graph(avg_stream):
    time_axis = list(range(len(avg_stream)))
    plt.plot(time_axis, avg_stream)
    plt.title('Moving Average output')
    plt.xlabel('Line Number')
    plt.ylabel('Bytes transferred')
    plt.savefig("test.png")

def main():
    n = 4
    display_graph(moving_average(n))

if __name__ == "__main__":
    main()