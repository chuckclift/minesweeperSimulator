#!/usr/bin/python3.4

import unittest

import minesweeper
from minesweeper import get_adjacent_tiles
from minesweeper import count_adjacent_group
from collections import namedtuple

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

    def test_only_flags_left(self):
        Tile = namedtuple("Tile", ["coord", "adj_mine_count", "adj_flagged",
                               "adj_clicked", "adj_unclicked"])
        t = Tile((1,1), 1, {}, {(0,1), (1,0), (2,0), (0,2), (2,1), (1,2), (2,2)}, {(0,0)})

        self.assertEqual(len(t.adj_unclicked), t.adj_mine_count - len(t.adj_flagged))

        
if __name__ == "__main__": 
    unittest.main()

