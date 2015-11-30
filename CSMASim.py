from __future__ import print_function

__author__ = 'JacobAMason'

import random
import matplotlib.pyplot as plt
from Queue import PriorityQueue
from decimal import *
import logging

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(message)s")

getcontext().prec = 6

def array_generator(size):
    return sorted([Decimal(random.randint(0,1000000))/1000000 for e in range(size)])


def determine_new_start_time(packet_st, packetDuration, probability):
    rng = random.uniform(0, 1)
    for i, p in enumerate(range(probability, 1+probability, probability)):
        if rng < p:
            return (i+1)*packetDuration


def count_successful_packets_persistent(start_times, p):
    packetDuration = Decimal("0.001")
    delay = Decimal("0.000001")
    # packetDuration = 100
    # delay = 1
    used_time = packetDuration  # Count the first packet
    unused_time = Decimal("0.0")
    free_time = start_times[0] + packetDuration
    hasCollision = False
    Q = PriorityQueue()
    for each in start_times[1:]:
        Q.put((each, False))

    while not Q.empty():
        packet_st, isRetransmit = Q.get()

        previousPacket_st = free_time - packetDuration

        logging.debug("packet Tx: %f %s %f %s %s", packet_st, isRetransmit, previousPacket_st,
              previousPacket_st <= packet_st, packet_st < previousPacket_st + delay)


        if isRetransmit:
            # This packet is a second or later attempt, so we weigh the probability it sends
            if random.uniform(0, 1) > p:
                logging.info("Retransmitted packet decided not to send: %f", p)
                Q.put((packet_st + packetDuration, True))
                continue

        # this packet is sent when nothing else is transmitting.
        if free_time + delay <= packet_st:
            if not isRetransmit:
                unused_time += (packet_st - free_time - delay)
            used_time += packetDuration
            free_time = packet_st + packetDuration
            logging.debug("packet sent")
            hasCollision = False
        # This packet is sent right after the previous and they collide
        elif previousPacket_st <= packet_st < previousPacket_st + delay:
            if not hasCollision:
                used_time -= packetDuration
                unused_time += (packet_st - free_time + 2*packetDuration)
                hasCollision = True
            free_time = packet_st + packetDuration
            logging.debug("collision %f %f", used_time, unused_time)
        # This packet is trying to be sent while there is another packet in use
        else:  # packet_st < free_time + delay
            logging.debug("reschedule: %f", free_time + delay)
            Q.put((free_time + delay, True))


    return used_time/(used_time + unused_time)


def simulate_persistent(p):
    for N in range(100, 3001, 200):
        array = array_generator(N)
        G = N/Decimal("1000")
        logging.debug("G:", G)
        throughput = count_successful_packets_persistent(array, p)
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
    for N in range(100, 5001, 100):
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
