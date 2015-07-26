#!/usr/bin/python3.4

import unittest

from minesweeper import get_adjacent_tiles, count_adjacent_group, permutation_agree
from minesweeper import Tile_theory

class my_test (unittest.TestCase):
    def test_get_adjacent_tiles(self):
        self.assertEqual({(1,2)}, get_adjacent_tiles((1,1), [(1,2), (12, 4)]))
        surround_set = {(0, 0), (0, 1), (0, 2), (1,0), (1, 2)
                        ,(2, 0), (2, 1), (2, 2)}
        self.assertEqual(surround_set, get_adjacent_tiles((1,1)
                        , surround_set))

    def test_count_adjacent_group(self):
        self.assertEqual(1, count_adjacent_group((1,1), [(1,2), (12, 4)]))
        surround_set = {(0, 0), (0, 1), (0, 2), (1,0), (1, 2)
                        ,(2, 0), (2, 1), (2, 2)}
        self.assertEqual(8, count_adjacent_group((1,1), surround_set))

    def test_permutations_agree(self):
        reference_permutation = {(1,2):1, (3,3):0, (1,1):1}
        test_permutation = {(1,2):0, (1,1):1, (2,2):0}
        agreement = permutation_agree(test_permutation, reference_permutation)
        self.assertTrue(not agreement)

    def test_tile_theory(self):
        test_theory = Tile_theory( {(2,3),(3,3),(4,3)}, 5, 0, 2) 
        other_theory = Tile_theory( {(2,3), (3,3)}, 3, 2, 3)

        test_theory.check_permutations(other_theory.possible_permutations)

        self.assertEqual(2, len(test_theory.possible_permutations))
 
if __name__ == "__main__": 
    unittest.main()

