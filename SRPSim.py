from __future__ import print_function

__author__ = 'JacobAMason'

import random
import matplotlib.pyplot as plt


def simulate(SRP_Window_Size, N, RTT, error_rate):
    sim_time = 0
    timeout = RTT
    packets_left_to_send = N - 1

    class Packet:
        def __init__(self, timeout):
            self.timeout = timeout
            self.ACK = random.uniform(0, 1) > error_rate*2

        def isTimedOut(self, simTime):
            return simTime >= self.timeout

        def resend(self, timeout):
            self.ACK = random.uniform(0, 1) > error_rate*2
            self.timeout += timeout

        def isACKd(self, simTime):
            return self.ACK and self.isTimedOut(simTime)

    SRP_queue = [Packet(timeout)]
    while SRP_queue:
        sim_time += 1
        # print("sim time", sim_time)
        ackd_packets = 0
        for packet in SRP_queue:
            if packet.isACKd(sim_time):
                ackd_packets += 1
                # print("ackd", ackd_packets)
            else:
                if packet.isTimedOut(sim_time):
                    packet.resend(timeout)
                break

        SRP_queue = SRP_queue[ackd_packets:]
        if (ackd_packets or SRP_Window_Size > len(SRP_queue)) and packets_left_to_send > 0:
            packets_left_to_send -= 1
            SRP_queue.append(Packet(sim_time + timeout))
            # print("send")

    return sim_time

if __name__ == "__main__":
    N = 1000
    RTT = 20
    error_rate = 0.001

    plt.axis([0, 50, 0, 1])
    plt.ion()
    plt.show()

    for windowSize in range(1, 50):
        sim_time = simulate(windowSize, N, RTT, error_rate)
        throughput = N / float(sim_time)
        print("Final Simtime:", sim_time)
        print("Throughput:", throughput)
        plt.scatter(windowSize, throughput, marker='.')
        plt.pause(0.0001)

    print("Done!")
    while(True):
        plt.pause(0.0001)
