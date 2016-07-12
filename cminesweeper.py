#!/usr/bin/python3.4

from curses import wrapper
import time
# import minesweeper
from solvers import *
from game import *

def curses_solve(stdscr):
    BOARD_DIMENSIONS = (16, 30)
    MINE_NUMBER = 99
    my_board = Game_board(BOARD_DIMENSIONS, MINE_NUMBER)


    while not my_board.game_over:
        time.sleep(0.1)
 
        decide(my_board)

        stdscr.clear()


        stdscr.addstr(0 , 1, "--" * ( BOARD_DIMENSIONS[0] + 2))
        for i in range(0, BOARD_DIMENSIONS[1]):
            row = "| "
            for j in range(0, BOARD_DIMENSIONS[0]):
                if (j, i) in my_board.clicked:
                    row += str(my_board.tile_values[(j, i)]) + " "
                elif (j, i) in my_board.flagged:
                    row += "# "
                else:
                    row += "  "
             
            stdscr.addstr(i + 1, 1, row + "|")
        stdscr.addstr(BOARD_DIMENSIONS[1] + 1, 1, "--" * (BOARD_DIMENSIONS[0] + 2))
        
        stdscr.addstr(10, 2 * BOARD_DIMENSIONS[0] + 5, "clicked: " + str(len(my_board.clicked)))
        stdscr.refresh()
         
def main(stdscr_curses):
    for i in range(0, 100):
        curses_solve(stdscr_curses)         
        time.sleep(2)

wrapper(main)
