from __future__ import print_function

__author__ = 'JacobAMason'

import random
import matplotlib.pyplot as plt


def array_generator(size):
    return sorted([random.uniform(0, 1) for e in range(size)])


def count_successful_packets_persistent(array, p):
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


def simulate_persistent(p):
    for N in range(1000, 5001, 100):
        array = array_generator(N)
        throughput = count_successful_packets_persistent(array, p)
        G = N/1000.0
        yield (G, throughput)


def insert_in_sorted_order(array, e):
    array.append(e)
    return sorted(array)


def count_successful_packets_nonpersistent(array):
    packetDuration = 0.001
    delay = 0.000001
    successes = 0
    fails = 0

    free_time = 0

    # TX = []

    while array:
        packet_st = array.pop(0)

        # check to see if there is already a packet in the air
        # if there is, put this packet back in the queue
        if free_time + delay - packetDuration <= packet_st <= free_time + delay:
            packet_st += packetDuration*random.uniform(1,400)
            array = insert_in_sorted_order(array, packet_st)
            # print("replaced packet")
        elif packet_st < free_time + delay - packetDuration:
            # this packet transmitted too quickly after the previous one and
            # has caused a collision.
            # update the next free time to the end of this packet
            successes -= packetDuration + delay  # roll off the success generated for the previous packet
            fails += packet_st - free_time + delay
            free_time = packet_st + packetDuration
            # TX.pop()
            # print("Collision")
        else:  # the air is clear, so let's transmit
            fails += packet_st - free_time - delay
            free_time = packet_st + packetDuration
            successes += packetDuration + delay
            # TX.append(packet_st)
            # print("TX")

    # print(TX)
    return successes/float(successes + fails)


def simulate_nonpersistent():
    for N in range(1000, 5001, 100):
        array = array_generator(N)
        throughput = count_successful_packets_nonpersistent(array)
        G = N/1000.0
        yield (G, throughput)


if __name__ == "__main__":
    plt.axis([0, 6, 0, 1.1])
    plt.ion()
    plt.show()

    for point in simulate_persistent(1):
        plt.scatter(*point, marker='.', color="red")
        plt.pause(0.0001)

    for point in simulate_persistent(0.5):
        plt.scatter(*point, marker='.', color="orange")
        plt.pause(0.0001)

    for point in simulate_persistent(0.1):
        plt.scatter(*point, marker='.', color="blue")
        plt.pause(0.0001)

    for point in simulate_persistent(0.01):
        plt.scatter(*point, marker='.', color="green")
        plt.pause(0.0001)

    for point in simulate_nonpersistent():
        plt.scatter(*point, color="black")
        plt.pause(0.0001)

    print("Done!")
    while(True):
        plt.pause(0.0001)
