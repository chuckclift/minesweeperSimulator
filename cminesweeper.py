#!/usr/bin/python3.4

from curses import wrapper
import time
import minesweeper

def curses_solve(stdscr):
    BOARD_DIMENSIONS = (16, 30)
    MINE_NUMBER = 99
    my_board = minesweeper.Game_board(BOARD_DIMENSIONS, MINE_NUMBER)


    while not my_board.game_over:
        time.sleep(0.1)
        previous_clicked = len(my_board.clicked)
        previous_flagged = len(my_board.flagged)
 
        minesweeper.decide(my_board)

        same_clicked = len(my_board.clicked) == previous_clicked
        same_flagged = len(my_board.flagged) == previous_flagged
    
        # if nothing has changed, guess
        if same_clicked and same_flagged:
            minesweeper.guess(my_board)
        stdscr.clear()


        stdscr.addstr(0 , 1, "* " * ( BOARD_DIMENSIONS[0] + 2))
        for i in range(0, BOARD_DIMENSIONS[1]):
            row = "* "
            for j in range(0, BOARD_DIMENSIONS[0]):
                if (j, i) in my_board.clicked:
                    row += str(my_board.tile_values[(j, i)]) + " "
                elif (j, i) in my_board.flagged:
                    row += "# "
                else:
                    row += "  "
             
            stdscr.addstr(i + 1, 1, row + "*")
        stdscr.addstr(BOARD_DIMENSIONS[1] + 1, 1, "* " * (BOARD_DIMENSIONS[0] + 2))
        
        stdscr.refresh()
         
def main(stdscr_curses):
    for i in range(0, 100):
        curses_solve(stdscr_curses)         

wrapper(main)
