from __future__ import print_function

__author__ = 'JacobAMason'

import random
import matplotlib.pyplot as plt


def array_generator(size):
    return sorted([random.uniform(0, 1) for e in range(size)])


def count_successful_packets(array, p):
    packetDuration = 0.001
    roundedArray = [int(x/packetDuration) for x in array]
    successes = 0
    fails = 0

    isBusy = False
    collision = False

    for i in range(len(roundedArray)-1):
        previousPacket_window = roundedArray[i]
        currentPacket_window = roundedArray[i+1]
        if currentPacket_window > previousPacket_window:
            if isBusy and not collision:
                successes += 1
            elif isBusy and collision:
                fails += 1
            isBusy = False
            collision = False

        if random.uniform(0, 1) <= p:
            if isBusy:
                collision = True
            else:
                isBusy = True

    return successes/float(successes + fails)


def simulate(p):
    for N in range(1000, 5001, 100):
        array = array_generator(N)
        throughput = count_successful_packets(array, p)
        G = N/1000.0
        #throughput = successes/1000.0
        yield (G, throughput)



if __name__ == "__main__":
    plt.axis([0, 6, 0, 1.1])
    plt.ion()
    plt.show()

    for point in simulate(1):
        plt.scatter(*point, marker='.', color="red")
        plt.pause(0.0001)

    for point in simulate(0.5):
        plt.scatter(*point, marker='.', color="orange")
        plt.pause(0.0001)

    for point in simulate(0.1):
        plt.scatter(*point, marker='.', color="blue")
        plt.pause(0.0001)

    for point in simulate(0.01):
        plt.scatter(*point, marker='.', color="green")
        plt.pause(0.0001)


    print("Done!")
    while(True):
        plt.pause(0.0001)
