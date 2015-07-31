#!/usr/bin/python3.4

import unittest

import minesweeper
from minesweeper import get_adjacent_tiles, count_adjacent_group
from minesweeper import Tile_theory, permutation_agree


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

        test_theory = Tile_theory( {(2,3),(3,3),(4,3)}, 5, 0, 2) 
        agreement = permutation_agree(test_permutation, reference_permutation)
        self.assertTrue(not agreement)

        reference_permutation = {(1,0):0, (0,0):1}
        test_permutation = {(1,0):1, (2,0):0, (0,0):1}
        
        agreement = permutation_agree(test_permutation, reference_permutation)
        self.assertTrue(not agreement)

        reference_permutation = {(1,0):1, (0,0):1}
        test_permutation = {(1,0):1, (2,0):0, (0,0):1}
        agreement = permutation_agree(test_permutation, reference_permutation)
        self.assertTrue(agreement)



        
    def test_tile_theory(self):
        """
            Testing this situation
           ##   ~   ~ = wall
            4   ~   # = flag
            #321~
            #200~
            ~~~~~

            Looking at the area around the 3 and the
            2 to its right 
        """
        other_theory = Tile_theory( {(2,3), (3,3)}, 3, 2, 3)
        test_theory = Tile_theory( {(2,3),(3,3),(4,3)}, 5, 0, 2) 

        test_theory.check_permutations(other_theory.possible_permutations)
        self.assertEqual(2, len(test_theory.possible_permutations))

        # example
        # *s*
        # 121
        board1 = ['*s*','121']
        board = minesweeper.Text_generated_board(board1)
        test_theory = Tile_theory(board.unclicked, len(board.clicked),
                                  len(board.flagged), board.get_mine_count())
        
 
if __name__ == "__main__": 
    unittest.main()

