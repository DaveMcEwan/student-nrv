import sys

# Need a list to store the previous n values
# There are no fixed length python lists

def moving_average(window_size):
    window = []
    for bytes in map(str.rstrip, sys.stdin):
        window.append(int(bytes))
        if (len(window)) > window_size:
            window.pop(0)
        print(sum(window)/len(window))

# def display_graph():
    #

def main():
    n = 4
    moving_average(n)
    # display_graph()

if __name__ == "__main__":
    main()