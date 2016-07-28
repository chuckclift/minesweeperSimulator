#!/usr/bin/env python3
 
import random
import time
from itertools import product 
from multiprocessing import Pool
from utils import * 
from game import * 

       
     
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

    if zero_adj_mine_tiles or  all_mines_found_tiles or only_flags_left_tiles:
        pass
    elif find_121(board):
        pass
    else:
        guess(board)

def is_121(tile, board):
    # is the adjusted value 2?
    if not adjust_value(tile, board.clicked[tile],  board.flagged) == 2:
        return False

    # does it have 3 adjacent unclicked?
    if not count_adjacent_group(tile, board.unclicked) == 3:
        return False 

    # does it have 2 adjacent adjusted 1's?
    adjacent = {a: adjust_value(a, board.clicked[a],  board.flagged) 
                        for a in get_adjacent_tiles(tile, board.clicked)}
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
    board = len(board.clicked) + len(board.unclicked)
    percent = int(100 * (clicked + flagged) / board)


    time.sleep(10)
    return percent 
 
def silent_solve(board):
    while not board.game_over:
        decide(board)

    clicked = len(board.clicked)
    flagged = len(board.flagged)
    board = len(board.clicked) + len(board.unclicked)
    percent = int(100 * (clicked + flagged) / board)
    return percent 

