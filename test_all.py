__author__ = 'JacobAMason'

import unittest
import AlohaSim


class TestAlohaSim(unittest.TestCase):
    def test_array_generator(self):
        size = 1000
        array = list(AlohaSim.array_generator(size))
        self.assertEqual(len(array), size)
        self.assertTrue(all([0 <= e <= 1 for e in array]))
        sortedArray = sorted(array)
        self.assertListEqual(sortedArray, array, "List is not sorted")

    def test_count_successful_packets_ALOHA(self):
        packet_duration = 1
        array = [0, 1, 3, 3.5, 5, 5.5, 7]
        successes = AlohaSim.count_successful_packets_ALOHA(array, packet_duration)
        self.assertEqual(successes, 3)

    def test_count_successful_packets_slottedALOHA(self):
        packet_duration = 1
        array = [0, 1, 2.5, 3, 3.5, 5, 5.5, 7]
        successes = AlohaSim.count_successful_packets_slottedALOHA(array, packet_duration)
        self.assertEqual(successes, 4)
