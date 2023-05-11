from unittest import TestCase

from graph import Digraph


class DigraphTestCase(TestCase):
    """Test Digraph class"""

    def test_find_strongly_connected_components(self):
        self.assertEqual(Digraph([
            []
        ]).find_strongly_connected_components(), set([
            frozenset([0])
        ]))

        self.assertEqual(Digraph([
            [1],
            [],
            [1],
        ]).find_strongly_connected_components(), set([
            frozenset([0]),
            frozenset([1]),
            frozenset([2]),
        ]))

        self.assertEqual(Digraph([
            [1, 2, 4],
            [0, 2, 3, 4, 6],
            [5],
            [1, 6],
            [6],
            [1],
            [5],
        ]).find_strongly_connected_components(), set([
            frozenset([0, 1, 2, 3, 4, 5, 6])
        ]))

        self.assertEqual(Digraph([
            [1, 2, 9],
            [2, 10],
            [4],
            [6, 9],
            [0],
            [3, 8],
            [10],
            [5],
            [0, 4, 7],
            [6],
            [9],
        ]).find_strongly_connected_components(), set([
            frozenset([0, 1, 2, 4]),
            frozenset([3]),
            frozenset([5, 7, 8]),
            frozenset([6, 9, 10]),
        ]))
