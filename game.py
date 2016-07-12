#!/usr/bin/env python3
 
import random
from collections import namedtuple
from utils import *

Tile = namedtuple("Tile", ["coord", "adj_mine_count", "adj_flagged",
                           "adj_clicked", "adj_unclicked"])
def create_tile(tile, board):
    value = board.tile_values[tile]
    adj_flagged = get_adjacent_tiles(tile, board.flagged)
    adj_clicked = get_adjacent_tiles(tile, board.clicked)
    adj_unclicked = get_adjacent_tiles(tile, board.unclicked)
    return Tile(tile, value, adj_flagged, adj_clicked, adj_unclicked)

class Game_board(object):
    def __init__(self, dimensions, MINE_COUNT):
        self._x_dim, self._y_dim = dimensions 
         
        # making a list of all of the coordinates 
        self._tile_coordinates = [(a, b) for a in range(0, self._x_dim)
                             for b in range(0, self._y_dim)]
 
        random.shuffle(self._tile_coordinates)
 
        self._mined = self._tile_coordinates[:MINE_COUNT]
        self.number_board = [count_adjacent_group(a, self._mined) 
                          for a in self._tile_coordinates]
 
        self._tile_values  = {key: value for (key, value)
                          in zip(self._tile_coordinates, self.number_board)} 
 
        self._flagged = set()
        self._clicked = set()
        self._unclicked = set(self._tile_coordinates[:])
        self.game_over = False

        for co, val in self._tile_values.items():
            if val == 0:
                for a in get_adjacent_tiles(co, self._unclicked):
                    self._clicked.add(a) 
                    self._unclicked.discard(a)
                break
                    
    def print_board_numbers(self):
        print("##########Board Numbers###########")
        for i in range(0, self._y_dim):
            print("row numbers " + str(self._y_dim))
            print("column numbers " + str(self._x_dim))
            row_values = [self._tile_values[j, i]
                         for j in range(0, self._x_dim)]
            print(" ".join(str(a) for a in row_values ))
 
    def print_clicked_tiles(self):
        print("##########Clicked Tiles#########")
        for i in range(0, self._y_dim):
            row = ""
            for j in range(0, self._x_dim):
                if (j, i) in self._mined and (j,i) in self._clicked:
                    row += "*"
                elif (j, i) in self._clicked: 
                    row +=  str(self._tile_values[(j, i)])
                elif (j, i) in self._flagged:
                    row += "#"
                else:
                    row += " "
            print(row)
        print("###############################")
        print("You have flagged " + str(len(self._flagged)))


    def print_mines_numbers(self):
        print("##########Mines and Numbers#########")
        for i in range(0, self._y_dim):
            row = "@"
            for j in range(0, self._x_dim):
                if (j, i) in self._mined:
                    row += "*"
                else:
                    row +=  str(self._tile_values[(j, i)])
            row += "@"
            print(row)
        print("###############################")
 
    def click_tile(self, location):
        if location in self._mined:
            self._clicked.add(location)
            self.game_over = True
            return True
        else:
            self._clicked.add(location) 
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
    def tile_values(self):
        return self._tile_values
 
    @tile_values.setter
    def tile_values(self, value):
        self._tile_values = value
 
    @property
    def tile_coordinates(self):
        return self._tile_coordinates
 
    @tile_coordinates.setter
    def tile_coordinates(self, value):
        self._tile_coordinates = value
 
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
        rows = [] 
        for r in board_rows:
            values_in_row = [a in r for a in "#*s012345678"]
            if any(values_in_row) and not " " in r:
                rows.append(r.strip())    

        self._x_dim = len(rows[0])
        self._y_dim = len(rows)

        self._tile_values = dict() 
        self._flagged = [] 
        self._clicked = [] 
        self._unclicked = [] 
        self._mined = [] 
        
        row_count = 0
        for r in rows:
            column_count = 0
            for c in list(r):
                if c == '*':
                    self._mined.append((column_count,row_count))
                    self._unclicked.append((column_count, row_count))
                elif c == '#':
                    self._flagged.append((column_count,row_count))
                    self._mined.append((column_count, row_count))
                elif c == 's':
                    self._unclicked.append((column_count,row_count))
                else:
                    self._tile_values[column_count, row_count] = int(c)
                    self._clicked.append((column_count, row_count))
                column_count += 1
            row_count += 1  

        uncounted_spaces = self._mined + self._flagged + self._unclicked
        for i in uncounted_spaces:
            adjacent_mines = count_adjacent_group(i, self._mined)
            self._tile_values[i] = adjacent_mines
       
        self._tile_coordinates = list(self._tile_values)
        self._flagged = set(self._flagged)
        self._clicked = set(self._clicked)
        self._unclicked = set(self._unclicked)

        self.game_over = False


