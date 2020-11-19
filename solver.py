'''
file: solver.py
----------
This file contains the implementation for a minesweeper solver.
'''

import time
import random

'''
function: solve
----------
Returns a boolean indicating if the board was successfully solved.
'''
def solve(board, animate=False) -> bool:
    if animate: board.verbose = True
    
    firstMove = True
    lastLoopHadZeroMoves = False
    
    # grid cells that will not give any more info and should not be checked
    done = [[False for _ in range(board.n)] for _ in range(board.n)]
    
    while not board.lost and not board.won:
        # on the first move, choose the middle of the grid
        if firstMove:
            firstMove = False
            board.printState(board.printBoard)
            if animate: time.sleep(1)
            board.move((int(board.n / 2), int(board.n / 2)))
            continue
            
        nextMoves = findMoves(board, done)
        if len(nextMoves) > 0:
            # move
            for nextMove in nextMoves:
                board.move(nextMove)
                if animate: time.sleep(0.1)
                
        elif lastLoopHadZeroMoves:
            # make a guess on a random covered cell
            madeGuess = False
            while not madeGuess:
                row = random.randint(0, board.n - 1)
                col = random.randint(0, board.n - 1)
                if board.grid[row][col] == 'covered':
                    madeGuess = True
                    board.move((row, col))
            lastLoopHadZeroMoves = False
            if animate: time.sleep(0.1)
                    
        else:
            lastLoopHadZeroMoves = True
        
    return board.won
       
'''
function: countCell
----------
Returns two integers:
 - the number of covered cells among the neighbors of the cell at the given row
   and col.
 - the number of flagged cells among the neighbors of the cell at the given row
   and col.
'''
def countCell(board, row, col):
    coveredCount = 0
    flaggedCount = 0
    
    for r, c in board.getNeighbors(row, col):
        if board.isValid(r, c):
            if board.grid[r][c] == 'covered': coveredCount += 1
            elif board.grid[r][c] == 'flagged': flaggedCount += 1
            
    return coveredCount, flaggedCount

'''
function: flagAllNeighbors
----------
This function marks each of the covered neighbors of the cell at the given row
and col as flagged.
'''
def flagAllNeighbors(board, row, col):    
    for r, c in board.getNeighbors(row, col):
        if board.isValid(r, c) and board.grid[r][c] == 'covered':
            board.flag(r, c)

'''
function: coveredNeighbors
----------
This function returns a set containing all of the covered neighbors of the cell
at the given row and col
'''
def coveredNeighbors(board, row, col):
    neighbors = set()
    
    for r, c in board.getNeighbors(row, col):
        if board.isValid(r, c) and board.grid[r][c] == 'covered':
            neighbors.add((r, c))
    return neighbors

'''
function: findMoves
----------
This function returns a set containing (row, col) pairs of moves to be made on
the board at its given state. It follows a few logic rules to determine which
moves are valid:

 1. If the number on a cell minus the number of flagged neighbors equals the
    number of covered neighbors, the rest of the neighbors are mines, so they
    should be flagged.
    
 2. If the number on a cell minus the number of flagged neighbors equals zero,
    all mines in the neighborhood have been found, so it is safe to uncover all
    covered neighbors.
    
NOTE: There were more rules I considered in order to make the logic more
robust. This included creating a set of linked cells where I knew there was
exactly one mine among a certain set of cells. This would give more intuition
on which cells had to contain mines or had to be safe.
Then, as an ultimate form of logic, I could have computed the exact probability
of every cell containing a mine. Then, I would make moves on the cells that had
zero probability or the lowest probability if there were no more cells with
zero probability.
While these features would imrpove accuracy, they would also come at the cost
of increased runtime. In the end, I decided that I could not dedicate enough
time to implement these features.
'''
def findMoves(board, done):
    moves = set()
    for row in range(board.n):
        for col in range(board.n):
            # if a cell is done or covered, do not analyze it
            if done[row][col] or board.grid[row][col] == 'covered':
                continue
            coveredCount, flaggedCount = countCell(board, row, col)
            if coveredCount == 0 or \
               board.grid[row][col] == 'flagged' or \
               board.grid[row][col] == 'safe':
                done[row][col] = True
                continue
            if board.grid[row][col] - flaggedCount == coveredCount:
                # all uncovered neighbors are mines
                flagAllNeighbors(board, row, col)
            elif board.grid[row][col] - flaggedCount == 0:
                # safe to uncover all neighbors that are covered
                moves = moves.union(coveredNeighbors(board, row, col))
    return set(moves)
