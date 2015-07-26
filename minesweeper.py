#!/usr/bin/python3.4
 
import random
import time
from itertools import permutations
 
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
 
class Tile_theory(object):
    def __init__(self, unclicked, clicked_count, flagged_count, mine_count):
        uncounted_mines = mine_count - flagged_count
        mines = [1] * uncounted_mines

        empty_spaces = len(unclicked) - uncounted_mines 
        empty = [0] * empty_spaces 


        combinations = set([a for a in permutations(mines + empty) 
                       if len(a) == len(unclicked)])

        # assigning each possible permutation of mine values (1 or 0) to the
        # tile locations each row is a possible situation
        self._possible_permutations = [{s: m for s,m in zip(unclicked, p)}
                                         for p in combinations]


#        print("\n".join([ str(a) for a in self._possible_permutations]))

    def check_permutations (self, reference_permutations):
#        self._possible_permutations = [a for a in self._possible_permutations
#                                      if any([permutation_agree(a, ref) 
#                                     for ref in reference_permutations])]
        new_permutations = []
        for a in self._possible_permutations:
            agreement = [permutation_agree(a, ref) 
                         for ref in reference_permutations]

            # testing if each possibility agrees with at least one of the 
            # other theories.  otherwise, it is not included in the new list
            if any(agreement):
                new_permutations.append(a)

        self._possible_permutations = new_permutations
                                       
    @property
    def possible_permutations(self):
        return self._possible_permutations
 
    @possible_permutations.setter
    def possible_permutations(self, value):
        self._possible_permutations = value
 

def permutation_agree(test_permutation, reference_permutation):
    """
        takes in two dictionaries with the coordinates (as tuples)
        as the keys and with the mine values as the value (0 or 1).
        If they disagree on at least one value, this function
        returns a false
    """ 
    # if none of the dictionary keys match, the permutations can not disagree,
    # so the intersection of the two sets is checked.  If there is no overlap,
    # then the permutations agree (so true is returned).
    permutation_set = set(test_permutation)
    reference_set = set(reference_permutation)
    intersection = permutation_set.intersection(reference_set)
    overlap = len(intersection) != 0
    if not overlap:
        return True

    any_disagreement = [False for a in intersection
                       if test_permutation[a] != reference_permutation[a]]

    if any_disagreement:
        return False
    else:
        return True  





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
 
    # if none of that works, just guess               
    guess(board)
 
def guess(board):
    random_pick = random.choice(list(board.unclicked))
    board.click_tile(random_pick)
    
         
 
def solve(board, mine_number):
    while not board.game_over:
#        time.sleep(0.1)
        previous_unclicked = len(board.unclicked)
 
        decide(board)
        board.print_clicked_tiles()
        print("Length of clicked: " + str(len(board.clicked)))
 
 
    if len(board.flagged) == mine_number:
        print("You've won, congratulations")
    else:
        print("Better luck next time")
        print("you only had %i mines left" % (mine_number - len(board.flagged)))
     
 
if __name__ == "__main__":
    for i in range(0, 10): 
        BOARD_DIMENSIONS = (30, 16)
        MINE_NUMBER = 99
        my_board = Game_board(BOARD_DIMENSIONS, MINE_NUMBER)
        solve(my_board, MINE_NUMBER)
     
 
