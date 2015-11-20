from __future__ import print_function

__author__ = 'JacobAMason'

import random
import matplotlib.pyplot as plt

def array_generator(size):
    return sorted([random.uniform(0, 1) for e in range(size)])


def generate_packet_durations(resolution, packetsToSend, maxG):
    return frange(resolution, (maxG/packetsToSend) + resolution, resolution)


# https://stackoverflow.com/questions/4189766
def frange(start, stop, step):
    while start < stop:
        yield start
        start += step


def count_successful_packets_ALOHA(array, packet_duration):
    # Check first packets
    successes = 1 if array[1] - array[0] >= packet_duration else 0

    # Check middle packets
    for packet in range(1, len(array)-2):
        if is_ALOHA_transmission_successful(array, packet, packet_duration):
            successes += 1

    # Check last packet
    successes += 1 if array[-1] - array[-2] >= packet_duration else 0

    return successes


def count_successful_packets_slottedALOHA(array, packet_duration):
    roundedArray = [int(x/packet_duration) for x in array]

    # Check first packets
    successes = 1 if array[0] != array[1] else 0

    # Check middle packets
    for packet in range(len(roundedArray)-2):
        if roundedArray[packet-1] < roundedArray[packet] < roundedArray[packet+1]:
            # print("pack", packet, roundedArray[packet-1], roundedArray[packet], roundedArray[packet+1])
            successes += 1

    # Check last packet
    successes += 1 if array[-1] != array[-2] else 0

    return successes


def is_ALOHA_transmission_successful(array, packet, packet_duration):
    return array[packet] - array[packet - 1] >= packet_duration and array[packet + 1] - array[packet] >= packet_duration


def simulate(array, resolution, maxG, count_successful_packets):
    packetsToSend = len(array)
    for packet_duration in generate_packet_durations(resolution, packetsToSend, maxG):
        successes = count_successful_packets(array, packet_duration)
        throughput = successes * packet_duration
        G = packet_duration * packetsToSend
        yield (G, throughput)


if __name__ == "__main__":
    maxG = 3.0
    plt.axis([0, maxG, 0, 0.5])
    plt.ion()
    plt.show()
    array = array_generator(1000)
    for point in simulate(array, 0.00001, maxG, count_successful_packets_ALOHA):
        plt.scatter(*point, marker='.')
        plt.pause(0.0001)

    for point in simulate(array, 0.00001, maxG, count_successful_packets_slottedALOHA):
        plt.scatter(*point, marker='.', color="red")
        plt.pause(0.0001)

    print("Done!")
    while(True):
        plt.pause(0.0001)
