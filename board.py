'''
file: board.py
----------
This file contains the implementation for a minesweeper board.
'''
import random

'''
class: Board
----------
This class describes the properties of a minesweeper board.
'''
class Board:
    '''
    function: __init__
    ----------
    This function initializes a Board object.

    Members:
        - self.n         : dimension
        - self.num_mines : number of mines to put on the board
        - self.grid      : state of the board visible to player
        - self.mines     : locations of all mines (not visible to player)
        - self.verbose   : determines if boards are printed to console or not
    '''
    def __init__(self, n, num_mines, verbose=False):
        self.n = n
        self.num_mines = num_mines
        self.grid = [['covered' for i in range(n)] for j in range(n)]
        self.mines = [[None for i in range(n)] for j in range(n)]
        self.initializeMines()
        self.lost = False
        self.won = False
        self.firstMove = True
        self.verbose = verbose
        self.printState(self.printBoard)
    
    '''
    function: isValid
    ----------
    Returns a boolean indicating if the cell at the given row and col is within
    the boundaries of the board.
    '''
    def isValid(self, row, col):
        return row >= 0 and row < self.n and col >= 0 and col < self.n
    
    '''
    function: getNeighbors
    ----------
    Returns a list of locations for the neighbors of the cell at the given row
    and column
    '''
    def getNeighbors(self, row, col):
        return [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                (row, col - 1), (row, col + 1),
                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    '''
    function: initializeMines
    ----------
    Places the right number of mines on the board.
    '''
    def initializeMines(self):
        minesPlaced = 0
        while minesPlaced < self.num_mines:
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            # check if there is already a mine there
            if not self.mines[row][col]:
                self.mines[row][col] = 'mine'
                minesPlaced += 1
                
    '''
    function: moveMine
    ----------
    This function is called if the player's first move is on a mine. It
    relocates the mine so that the game can be played.
    '''
    def moveMine(self, row, col):
        minesPlaced = 0
        while minesPlaced < 1:
            r = random.randint(0, self.n - 1)
            c = random.randint(0, self.n - 1)
            # check if there is already a mine there
            if not self.mines[r][c]:
                self.mines[r][c] = 'mine'
                minesPlaced += 1
        # remove the old mine
        self.mines[row][col] = None
        
    '''
    function: flag
    ----------
    This function marks the cell at the given row and col as flagged.
    '''
    def flag(self, row, col):
        if self.isValid(row, col):
            if self.grid[row][col] == 'covered':
                self.grid[row][col] = 'flagged'
            elif self.grid[row][col] == 'flagged':
                self.grid[row][col] = 'covered'
            if self.verbose: print()
            self.printState(self.printBoard)
    
    '''
    function: gameLost
    ----------
    Returns a boolean indicating if a move on the given row and col will result
    in the game being lost.
    '''
    def gameLost(self, row, col):
        return self.mines[row][col] == 'mine'
    
    '''
    function: lose
    ----------
    Called when the game is lost.
    '''
    def lose(self):
        if self.verbose: print('You lose \U0001F92C\n') # 🤬
        self.lost = True
        self.printState(self.printGameOverBoard)
    
    '''
    function: gameWon
    ----------
    Returns a boolean indicating if the current state of the board is
    a winning game.
    '''
    def gameWon(self):
        for row in range(self.n):
            for col in range(self.n):
                # if there is an uncovered blank space
                if self.grid[row][col] == 'covered' or \
                   self.grid[row][col] == 'flagged':
                    if not self.mines[row][col]:
                        return False
        return True
    
    '''
    function: win
    ----------
    Called when the game is won.
    '''
    def win(self):
        if self.verbose: print('You win \U0001F3C6\n') # 🏆
        self.won = True
        self.printState(self.printGameOverBoard)
    
    '''
    function: countMines
    ----------
    Counts the number of mines adjacent to the cell at the given row and col.
    If there are no mines, this function returns the string 'safe'. Otherwise,
    it returns the number of mines as an integer.
    '''
    def countMines(self, row, col):
        count = 0
                
        for r, c in self.getNeighbors(row, col):
            if self.isValid(r, c) and self.mines[r][c]:
                count += 1
                
        if count == 0: return 'safe'
        
        return count
    
    '''
    function: moveHelper
    ----------
    This is a recursive function that processes cells for one origin
    move. When a move is made on a cell that has no neighboring mines,
    all of the adjacent cells are recursively processed as well.
    '''
    def moveHelper(self, row, col, processed):
        # process the current location
        self.grid[row][col] = self.countMines(row, col)
        processed[row][col] = True
        # base case
        if not self.grid[row][col] == 'safe':
            return
            
        # recursive case: current location is empty -> process all neighbors        
        for r, c in self.getNeighbors(row, col):
            if self.isValid(r, c) and not self.mines[r][c] and not processed[r][c]:
                self.moveHelper(r, c, processed)
    
    '''
    function: move
    ----------
    Perfoms a move on the given cell.
    '''
    def move(self, cell):
        if self.verbose: print()
        row, col = cell
        
        # if the first move is on a mine, move it to a new location
        if self.firstMove:
            self.firstMove = False
            if self.mines[row][col]:
                self.moveMine(row, col)
    
        # if the given move results in a losing game
        if self.gameLost(row, col):
            self.grid[row][col] = 'lost'
            self.lose()
            # return because there is no need to recurse
            return
        
        processed = [[False for i in range(self.n)] for j in range(self.n)]
        self.moveHelper(row, col, processed)
        
        # if the given move results in a winning game
        if self.gameWon():
            self.win()
        # else, proceed with the game
        else:
            self.printState(self.printBoard)
    
    '''
    function: printState
    ----------
    General function used to print the state of the board to the console. This
    function takes in a function parameter, func, to determine what information
    to print out for each cell.
    '''
    def printState(self, func):
        if not self.verbose: return
        
        print('    ', end='')
        for i in range(self.n):
            if i < 10: print(i, end=' ')
            else: print(i, end='')
        print()
        print('  +', end='')
        for i in range(self.n + 1):
            print('--', end='')
        print('+', end='')
        print()
        
        for i in range(self.n):
            if i < 10: print(' ', end='')
            print(i, end='')
            print('|', end=' ')
            
            for j in range(self.n):
                func(i, j)
                
            print(' |', end='')
            if i < 10: print(' ', end='')
            print(i, end=' ')
            print()
            
        print('  +', end='')
        for i in range(self.n + 1):
            print('--', end='')
        print('+', end='')
        print()
        print('    ', end='')
        for i in range(self.n):
            if i < 10: print(i, end=' ')
            else: print(i, end='')
        print('\n')
    
    '''
    function: printGameOverBoard
    ----------
    This print function tells the printState function the board information to
    print while the game has not been won or lost.
    '''
    def printBoard(self, i, j):
        if self.grid[i][j] == 'safe':
            print('\u25A0', end = ' ') # ■
        elif self.grid[i][j] == 'covered':
            print('\U00002B1C', end = '') # ⬜
        elif self.grid[i][j] == 'flagged':
            print('\U0001F6A9', end = '') # 🚩
        else:
            print(self.grid[i][j], end = ' ') # number
    
    '''
    function: printGameOverBoard
    ----------
    This print function tells the printState function the board information to
    print after the game has been either won or lost.
    '''
    def printGameOverBoard(self, i, j):
        if self.grid[i][j] == 'safe':
            print('\u25A0', end = ' ') # ■
        elif self.grid[i][j] == 'lost':
            print('\U0001F92F', end = '') # 🤯
        elif self.grid[i][j] == 'covered' or self.grid[i][j] == 'flagged':
            if self.mines[i][j]:
                print('\U0001F4A3', end = '') # 💣
            else:
                print('\U00002B1C', end = '') # ⬜
        else:
            print(self.grid[i][j], end = ' ') # number
