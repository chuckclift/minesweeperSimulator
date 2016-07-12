#!/usr/bin/env python3
 
from itertools import product 

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
           
        

