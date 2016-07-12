#!/usr/bin/env python3
 
import time
from multiprocessing import Pool
from statistics import mean
import optparse

from game import *
from solvers import *



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
