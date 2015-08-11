#!/usr/bin/python3.4

import unittest

import minesweeper
from minesweeper import get_adjacent_tiles, count_adjacent_group


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

    def test_check_pattern(self):
        rows = ["000", "121", "*s*"]
        board = minesweeper.Text_generated_board(rows)
        self.assertTrue(minesweeper.check_pattern(board, (1,1),   ["ccc", "1@21", "*s*"]))
         
if __name__ == "__main__": 
    unittest.main()

