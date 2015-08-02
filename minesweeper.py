#!/usr/bin/python3.4
 
import random
import time
from itertools import permutations
from itertools import product 
 
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
        self._unclicked = set(self._tile_coordinates.copy())
        self.game_over = False
        
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
               if (j, i) in self._clicked:
                   row +=  str(self._tile_values[(j, i)])
               elif (j, i) in self._flagged:
                   row += "#"
               else:
                   row += " "
            print(row)
        print("###############################")
        print("You have flagged " + str(len(self._flagged)))
 
    def click_tile(self, location):
        if location in self._mined:
            print("Game Over")
            self.game_over = True
            return True
        else:
            self._clicked.add(location) 
            self._unclicked.discard(location)
            print(len(self._clicked))
            return False
 
    def flag_tile(self, location):
        self._flagged.add(location)
        self._unclicked.discard(location) 
 
        win = all([a in self._flagged for a in self._mined])
        if win:
            print("you've won")
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



#######################################################
###  Utility Functions              ###################
#######################################################
def get_adjacent_tiles(point_location, group_locations):
    """
         returns a set of points that are adjacent to the 
         point_location value based on the group_locations list.
         The group locations set should be a set of tuples
         of the same type as the first function arguement
    """
 
    if len(group_locations) == 0:
        return {}
 
    x, y = point_location
    adjustments = {(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1)
                  ,(1, -1)}
 
    adjacent_tiles = {(x + v, y + w) for v, w in adjustments}
    return adjacent_tiles.intersection(group_locations)
     

def count_adjacent_group(point_location, group_locations):
    """
         finds out the number of points that are adjacent to the 
         point_location value based on the group_locations set.
         The group locations list should be a list of tuples
         of the same type as the first function arguement
    """
    adjacent_tiles = get_adjacent_tiles(point_location, group_locations)
    return len(adjacent_tiles)

def theory_valid(theory, chunk,  board):
    """
        tests a single theory based on whether each clicked
        tile has the required number of adjacent mines.
    """
    for i in chunk:
        adjacent_theory_values = [theory[a] for a in
                                 get_adjacent_tiles(i, theory)]
        
        theoretical_sum = (sum(adjacent_theory_values) +
                          count_adjacent_group(i, board.flagged))
        agree = theoretical_sum == board.tile_values[i]
        if not agree:
            return False
    return True

def chunk_surfaces(board):
    surfaces = []
    current_surface = set()
    unchunked_tiles = {a for a in board.clicked 
                      if count_adjacent_group(a, board.unclicked) > 0}
    for _ in range(0, len(unchunked_tiles)):
        new_start_point = unchunked_tiles.pop()
        new_surface = get_surface(new_start_point,  unchunked_tiles)
        surfaces.append(new_surface) 
        unchunked_tiles = unchunked_tiles - new_surface

        if len(unchunked_tiles) == 0:
            return surfaces
    return surfaces 
        
def get_surface(start_tile, unchunked_tiles):
    """
        Given a start tile and unchunked tiles, it 
    """
    chunked_surface = {start_tile}
    previous_surface = set()

    while len(chunked_surface) > len(previous_surface):
        previous_surface = chunked_surface.copy()

        new_edge = set()

        # getting the tiles at the "edge" of the chunk
        for i in chunked_surface:
            adjacent_tiles = set(get_adjacent_tiles(i, unchunked_tiles))
            new_tiles = adjacent_tiles.difference(chunked_surface)
            new_edge.update(new_tiles)

        chunked_surface.update(new_edge)

    return chunked_surface
    


#################################################
##     Solution functions                ########
#################################################
def decide(board):
    if len(board.clicked) == 0:
        random_pick = random.choice(list(board.unclicked))
        board.click_tile(random_pick)
    else:
        for i in board.clicked:
            adjacent_unclicked = count_adjacent_group(i, board.unclicked) 
            cell_complete = adjacent_unclicked == 0

            if not cell_complete:
                adjacent_mines = board.tile_values[i]
                unclicked_tiles =  get_adjacent_tiles(i, board.unclicked)

                if adjacent_mines == 0:
                    for a in unclicked_tiles:
                        board.click_tile(a)
                adjacent_flagged = count_adjacent_group(i, board.flagged)
                adjacent_clicked = count_adjacent_group(i, board.clicked) 
                
                mines_found = adjacent_mines == adjacent_flagged 
            
                if mines_found:
                    for a in unclicked_tiles:
                        board.click_tile(a)
                    return 
                elif adjacent_flagged + adjacent_unclicked == adjacent_mines :
                    for a in unclicked_tiles:
                        board.flag_tile(a)
                    return 
    theory_guess(board) 
    # if none of that works, just guess               


def theory_guess(board):
    """
        Decides the best move by building theories about small groups
        of tiles, and making moves based on those theories.
    """
    board_surfaces = chunk_surfaces(board)
    for i in board_surfaces:
        unclicked_tiles = board.unclicked

        # getting the corresponding unclicked surface
        adjacent_unclicked = [get_adjacent_tiles(a, unclicked_tiles) for a in i] 
        adjacent_unclicked = {a for b in adjacent_unclicked for a in b}
        if len(adjacent_unclicked) > 17:
            guess(board)
            return  

        # build theories of where mines are
        possibilities = product([0,1], repeat=len(adjacent_unclicked)) 
        theories = [{k:v for k,v in zip(adjacent_unclicked, p)} 
                     for p in possibilities]

        # test corresponding theories and keep the good ones
        good_theories = [a for a in theories if theory_valid(a, i,  board)]


        if len(good_theories) == 1:
        # if there is only one good theory, click all of the mine-free
        # tiles and flag all of the mined tiles
            for i in good_theories[0]:
                if good_theories[0][i] == 1:
                    board.flag_tile(i)
                else:
                    board.click_tile(i)
        else:
        # otherwise, calculate the probabilities the spaces
        # being mined based on those theories
            tile_probabilities = dict()
            for tile in adjacent_unclicked:
                mines = 0
                tiles = 0
                for theory in good_theories:
                    if tile in theory:
                        tiles += 1
                        mines += theory[tile]


                # if a space has a mine in all theories, flag it 
                if mines / tiles == 1:
                    board.flag_tile(tile)
                    return
                # If a space is mine-free in all theories, click it
                elif mines == 0:
                    board.click_tile(tile)
                    return
                    
                tile_probabilities[tile] = mines / tiles        

            # educated guessing
            average_probability = len(board.unclicked) / board.get_mine_count()
            
            probabilities = {tile_probabilities[a]:a for a in tile_probabilities}
           
            lowest = min(probabilities)
            if lowest < average_probability:
                best_tile = probabilities[lowest]                 
                board.click_tile(best_tile)
            else:
                guess(board)


def guess(board):
    if len(board.unclicked) > 0:
        random_pick = random.choice(list(board.unclicked))
        board.click_tile(random_pick)
    
def solve(board):
    mine_number = board.get_mine_count()
    while not board.game_over:
        time.sleep(0.1)
        previous_unclicked = len(board.unclicked)
 
        decide(board)
        board.print_clicked_tiles()
        print("Length of clicked: " + str(len(board.clicked)))
 
 
    if len(board.flagged) == mine_number:
        print("\n".join([str(a) for a in board.flagged]))
        print("You've won, congratulations")
    else:
        print("Better luck next time")
        print("you only had %i mines left" % (mine_number - len(board.flagged)))

 
if __name__ == "__main__":
    # running 2 simulations
    for i in range(0, 10): 
        
        BOARD_DIMENSIONS = (30, 16)
        MINE_NUMBER = 99
#        board_rows = ['ssssssssss',
#                      'ss*sss*sss',
#                      'ssssssss*s',
#                      'ss*sssssss']  
#        board_rows = ['*s*','121']
#        my_board = Text_generated_board(board_rows)
        my_board = Game_board(BOARD_DIMENSIONS, MINE_NUMBER)
        
        solve(my_board)
     
 
