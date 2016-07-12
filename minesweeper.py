#!/usr/bin/env python3
 
import random
import time
from itertools import product 
from multiprocessing import Pool
import progressMap
from statistics import mean
import optparse
from collections import namedtuple

Tile = namedtuple("Tile", ["coord", "adj_mine_count", "adj_flagged",
                           "adj_clicked", "adj_unclicked"])
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



#######################################################
###  Utility Functions              ###################
#######################################################
def create_tile(tile, board):
    return Tile(tile, board.tile_values[tile], get_adjacent_tiles(tile, board.flagged),
                get_adjacent_tiles(tile, board.clicked), get_adjacent_tiles(tile, board.unclicked))


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
        adjacent_theory_values = [theory[a] for a in get_adjacent_tiles(i, theory)]
        
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
   

    while len(unchunked_tiles) > 0:
        new_start_point = unchunked_tiles.pop()
        new_surface = get_surface(new_start_point,  unchunked_tiles)
        if len(new_surface) < 10:
            surfaces.append(new_surface) 
        unchunked_tiles = unchunked_tiles - new_surface

    return surfaces 

        
def get_surface(start_tile, unchunked_tiles):
    """
        Given a start tile and unchunked tiles, it builds a chain of adjacent
        tiles and returns them
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

def find_good_theories(chunk, board):
    unclicked_tiles = board.unclicked
    
    # getting the corresponding unclicked surface
    adjacent_unclicked = [get_adjacent_tiles(a, unclicked_tiles)
                         for a in chunk] 
    adjacent_unclicked = {a for b in adjacent_unclicked for a in b}
    
    # build theories of where mines are
    possibilities = product([0,1], repeat=len(adjacent_unclicked)) 
    good_theories = []

    for p in possibilities:
        theory = dict()
        # generating theory of where the mines are
        for k,v in zip(adjacent_unclicked, p):
            theory[k] = v

        if theory_valid(theory, chunk, board):
            good_theories.append(theory)
            

    return good_theories


def adjacent_chunk(chunk, board):
    adjacent_unclicked = [get_adjacent_tiles(a, board.unclicked)
                         for a in chunk] 
    return {a for b in adjacent_unclicked for a in b}

def split_big_chunk(chunk, max_difference=0.3):   
    """
        Breaks a set of coordinates into two smaller sets of coordinates
    """
    if len(chunk) < 3:
        return chunk
    
    # this works on linear chunks (two non-connected ends)
    for split_point in chunk:
        test_chunk = chunk.copy()
        test_chunk.discard(split_point)
        start_points = get_adjacent_tiles(split_point, test_chunk) 

        if len(start_points) == 2:
            surface_1 = get_surface(start_points.pop(), test_chunk)
            surface_2 = get_surface(start_points.pop(), test_chunk)

            # distance from the "ideal" 50/50 split
            closeness = (len(surface_1) - len(surface_2)) / len(chunk)
            close_enough = abs(closeness) < max_difference

            if close_enough:
                # adding split point so the split point doesn't lose coverage
                surface_1.add(split_point)
                surface_2.add(split_point)

                return [surface_1, surface_2]

    # this works on round chunks
    for split_1 in chunk:
        for split_2 in chunk:
            test_chunk = chunk - {split_1, split_2}
            
            start_points = get_adjacent_tiles(split_1, test_chunk)

            if len(start_points) == 2:
                surface_1 = get_surface(start_points.pop(), test_chunk)
                surface_2 = get_surface(start_points.pop(), test_chunk)

                closeness = (len(surface_1) - len(surface_2)) / len(chunk)               
                close_enough = abs(closeness) < max_difference
                    
                if close_enough:
                    surface_1.add(split_1)
                    surface_1.add(split_2)
                    surface_2.add(split_1)
                    surface_2.add(split_2)
                    return [surface_1, surface_2]

def adjust_value(tile, board):
    return board.tile_values[tile] - count_adjacent_group(tile, board.flagged)

def finished(tile, board):
    return count_adjacent_group(tile, board.unclicked) == 0

def small_chunk(tile, board):
    return {a for a in get_adjacent_tiles(tile, board.clicked) if not finished(a,board)}
           
        
     
#################################################
##     Solution functions                ########
#################################################
def decide(board):
    tiles = (create_tile(c, board) for c in board.clicked)

    unfinished_tiles = [c for c in tiles if len(c.adj_unclicked) > 0]

    zero_adj_mine_tiles = [c.adj_unclicked for c in unfinished_tiles if c.adj_mine_count == 0]
    all_mines_found_tiles = [c.adj_unclicked for c in unfinished_tiles
                             if c.adj_mine_count == len(c.adj_flagged)]
    only_flags_left_tiles = [c.adj_unclicked for c in unfinished_tiles
                             if len(c.adj_unclicked) == c.adj_mine_count - len(c.adj_flagged)]

    for a in zero_adj_mine_tiles:
        [board.click_tile(b) for b in a]

    for a in all_mines_found_tiles:
        [board.click_tile(b) for b in a]

    for a in only_flags_left_tiles:
        [board.flag_tile(b) for b in a]

    if zero_adj_mine_tiles:
        pass
    if all_mines_found_tiles:
        pass
    if only_flags_left_tiles:
        pass
    elif find_121(board):
        pass
    else:
        guess(board)

def is_121(tile, board):
    # is the adjusted value 2?
    if not adjust_value(tile, board) == 2:
        return False

    # does it have 3 adjacent unclicked?
    if not count_adjacent_group(tile, board.unclicked) == 3:
        return False 

    # does it have 2 adjacent adjusted 1's?
    adjacent = {a: adjust_value(a, board) for a in get_adjacent_tiles(tile, board.clicked)}
    adjacent = {a:b for a,b in adjacent.items() if b == 1}
 
    if not len(adjacent) == 2:
        return False

    x,y = tile
    if (x+1,y) in adjacent and (x-1, y) in adjacent:
        return True
    elif (x, y+1) in adjacent and (x, y-1) in adjacent:
        return True
    else: 
        return False

def find_121(board):
    """
        Checks for a 121 pattern in the board
    """
    if len(board.clicked) == 0:
        return False
  
     
    one_two_ones = [a for a in board.clicked if is_121(a, board)]
#    return any([is_121(a, board) for a in board.clicked.copy()])

    if len(one_two_ones) == 0:
        return False

    new_chunks = [small_chunk(a,board)  for a in one_two_ones]

    good_theories = [find_good_theories(chunk, board) for chunk in new_chunks]

    if check_for_one_theory(board, good_theories, new_chunks):
        return True
    elif check_single_tile(board, good_theories, new_chunks):
        return True
    else:
        return False
        
def generate_theories(board):
    """
        Decides the best move by building theories about small groups
        of tiles, and making moves based on those theories.
    """
    clicked_chunks = chunk_surfaces(board)
    if len(clicked_chunks) == 0:
        return False
    
    too_big_chunks = [len(adjacent_chunk(i, board)) > 16 for i in clicked_chunks]

    if any(too_big_chunks):
        new_chunks = []
        while True: 
            new_chunks = []

            for i in clicked_chunks:
                if len(adjacent_chunk(i, board)) > 16:
                    split = split_big_chunk(i)
                    if split:
                        new_chunks.extend(split)
                        break
                else:
                    new_chunks.append(i)

            if len(clicked_chunks) == len(new_chunks):
                break

            clicked_chunks = new_chunks.copy()
                    
     
    good_theories = [find_good_theories(chunk, board) for chunk in clicked_chunks]

    if check_for_one_theory(board, good_theories, clicked_chunks):
        return True
    elif check_single_tile(board, good_theories, clicked_chunks):
        return True
    else:
        return False

def check_for_one_theory(board, theories, clicked_chunks):
    """
        Checks the theories to see if any chunk has only one theory referring
        to it.  If there is, then that one theory must be correct.  This function
        clicks all spaces the theory says are empty and flags all that the theory
        says are mined.
    """
    for theory_list in theories:
        if len(theory_list) == 1:
        # if there is only one good theory, click all of the mine-free
        # tiles and flag all of the mined tiles
            for t in theory_list[0]:
                if theory_list[0][t] == 1:
                    board.flag_tile(t)
                else:
                    board.click_tile(t)
            return True
    return False 


def check_single_tile(board, theories, clicked_chunks):
    tile_probabilities = dict()

    for chunk, theory_list in zip(clicked_chunks, theories):
       # otherwise, calculate the probabilities the spaces
        # being mined based on those theories
        adjacent_unclicked = adjacent_chunk(chunk, board)
        for tile in adjacent_unclicked:
            mines = 0
            tiles = 0
            for theory in theory_list:
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

    probability_guess(board, tile_probabilities) 


def probability_guess(board, tile_probabilities):
    if len(tile_probabilities) == 0:
        guess(board)
        return False

    average_probability = board.get_mine_count() / len(board.unclicked)  
    probabilities = {tile_probabilities[a]:a for a in tile_probabilities}
       
    lowest = min(probabilities)
    if lowest < average_probability:
        best_tile = probabilities[lowest]                 
        board.click_tile(best_tile)
        return True
    else:
        return False

def guess(board):
    random_pick = random.choice(list(board.unclicked))
    board.click_tile(random_pick)
    
def visual_solve(board):
    mine_number = board.get_mine_count()

    while not board.game_over:
        time.sleep(0.1)
        decide(board)
        board.print_clicked_tiles()
        print("Length of clicked: " + str(len(board.clicked)))


 
    if len(board.flagged) == mine_number:
        print("You've won, congratulations")
    else:
        print("Better luck next time")
        print("you had %i mines left" % (mine_number - len(board.flagged)))
        print("There were ", str(mine_number), "mines total")

    clicked = len(board.clicked)
    flagged = len(board.flagged)
    board = len(board.tile_values)
    percent = int(100 * (clicked + flagged) / board)


    time.sleep(10)
    return percent 
 


def silent_solve(board):
    while not board.game_over:
        decide(board)

    clicked = len(board.clicked)
    flagged = len(board.flagged)
    board = len(board.tile_values)
    percent = int(100 * (clicked + flagged) / board)
    return percent 

def main():
    parser = optparse.OptionParser()
    parser.add_option("-m", action="store", default="p",
                      help="""Method of simulation p for processes,
                            v for visual, s for silent, and b for
                            progress bar""")
    parser.add_option("-s", action="store", type="int", default=100,
                      help="The number of simulations")
    parser.add_option("-p", action="store", type="int", default=8,
                      help="""the number of processes (if process option
                           is chosen)""")
    options, args = parser.parse_args()

    BOARD_DIMENSIONS = (30, 16)
    MINE_NUMBER = 99
    progress_scores = [] 
    SIMULATIONS =   options.s 
    boards = [Game_board(BOARD_DIMENSIONS, MINE_NUMBER) for i in range(SIMULATIONS)]

    probabilities = []
    start = time.time()
    # choosing how the solution will be performed and choosing output method
    if options.m == "p":
        solvers = Pool(options.p)
        probabilities = solvers.map(silent_solve, boards)
    elif options.m == "v":
        probabilities = [visual_solve(b) for b in boards]
    elif options.m == "s":
        probabilities = [silent_solve(b) for b in boards]
    elif options.m == "b":
        probabilities = progressMap.status_bar(silent_solve, boards)
    elapsed = time.time() - start

    probabilities.sort()

    graph_values = []
    for i in range(20):
        low = i * 5
        high = i*5 + 5
        total = sum([1 for a in probabilities if a >= low and a < high])
        percent = int(100 *   total /  SIMULATIONS) 
        label = str(low) + "-" + str(high) + ":"
        print(label, percent, "%")

    print("Average: ", round(mean(probabilities), 2))
    print("over 95%: ",sum([1 for a in probabilities if a > 95]))
    print("won: ", sum([1 for a in probabilities if a == 100])) 
    print("Simulations:",  options.s) 
    print("Elapsed time:", round(elapsed, 2))
    if options.m == "p":
        print("Processes:", options.p)

if __name__ == "__main__":
    main()
