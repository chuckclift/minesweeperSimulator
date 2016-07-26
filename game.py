#!/usr/bin/env python3
 
import random
from collections import namedtuple
from utils import *

Tile = namedtuple("Tile", ["coord", "adj_mine_count", "adj_flagged",
                           "adj_clicked", "adj_unclicked"])
def create_tile(tile, board):
    value = board._clicked[tile]
    adj_flagged = get_adjacent_tiles(tile, board.flagged)
    adj_clicked = get_adjacent_tiles(tile, board.clicked)
    adj_unclicked = get_adjacent_tiles(tile, board.unclicked)
    return Tile(tile, value, adj_flagged, adj_clicked, adj_unclicked)

class Game_board(object):
    def __init__(self, dimensions, MINE_COUNT, first_click):
        self._x_dim, self._y_dim = dimensions 
         
        self._unclicked  = {(a, b) for a in range(0, self._x_dim)
                                   for b in range(0, self._y_dim)} - {first_click}

        self._mined = random.sample(self._unclicked, MINE_COUNT)

        self._flagged = set()
        self._clicked = {first_click: count_adjacent_group(first_click, self._mined)}
        self.game_over = False
 
    def print_clicked_tiles(self):
        print("##########Clicked Tiles#########")
        for i in range(0, self._y_dim):
            row = ""
            for j in range(0, self._x_dim):
                if (j, i) in self._mined and (j,i) in self._clicked:
                    row += "*"
                elif (j, i) in self._clicked: 
                    row +=  str(self._clicked[(j, i)])
                elif (j, i) in self._flagged:
                    row += "#"
                else:
                    row += " "
            print(row)
        print("###############################")
        print("You have flagged " + str(len(self._flagged)))

    def click_tile(self, location):
        if location in self._mined:
            self._clicked[location] = "*"
            self.game_over = True
            return True
        else:
            self._clicked[location] = count_adjacent_group(location, self._mined)     # .add(location, ) 
            self._unclicked.discard(location)

            win = len(self._unclicked) == 0
            if win:
                self.game_over = True
            return False
 
    def flag_tile(self, location):
        self._flagged.add(location)
        self._unclicked.discard(location) 
        win = len(self._unclicked) == 0

        if win:
            self.game_over = True
    def get_mine_count(self):
        return len(self._mined)
    def game_over(self):
        return self.game_over 
 
    @property
    def flagged(self):
        return self._flagged
 
    @flagged.setter
    def flagged(self, value):
        self._flagged = value
 
    @property
    def unclicked(self):
        return self._unclicked
 
    @unclicked.setter
    def unclicked(self, value):
        self._unclicked = value
 
    @property
    def clicked(self):
        return self._clicked
 
    @clicked.setter
    def clicked(self, value):
        self._clicked = value
 
    @property
    def x_dim(self):
        return self._x_dim
 
    @x_dim.setter
    def x_dim(self, value):
        self._x_dim = value
 
    @property
    def y_dim(self):
        return self._y_dim
 
    @y_dim.setter
    def y_dim(self, value):
        self._y_dim = value

class Text_generated_board(Game_board):
    def __init__(self, board_rows):
        """
            a board is generated using input text rather than 
            dimensions and mine counts.  Each row is contained
            in a string.

            * = unflagged mine
            # = flagged mine
            1,2,...,8 = clicked tile
            s = unclicked tile
        
            example: 
            rows = ["121","*s*"]
            board = Text_generated_board(rows)
            solve(board)
        """
        values = {}
        for y, row in enumerate(board_rows):
            for x, value in enumerate(row):
                values[(x, y)] = value

        self._clicked = {a:b for a, b in values.items() if b in "012345678"}
        self._unclicked = {a for a, b in values.items() if b == "s"}
        self._flagged = {a for a,b in values.items() if b == "#"}
        self._mined = {a for a, b in values.items() if b == "*"}

        self._x_dim = len(board_rows[0])
        self._y_dim = len(board_rows)

        self.game_over = False

