'''
file: play
----------
This file allows for an interactive version of minesweeper for a user to play
through the command line.
'''

from board import Board
import argparse

'''
function: isValidInput
----------
Returns true if the input string is a valid input for a board size of n.
Valid moves include a flag move and a regular move.
 - a regular move should be of the format 'i j'
 - a flag move should be of the format 'flag i j'
where 0 <= i, j < n
'''
def isValidInput(input, n):
    tokenized = input.split(' ')
    
    if len(tokenized) == 2: # regular move
        if not tokenized[0].isnumeric() or not tokenized[1].isnumeric(): return False
        if int(tokenized[0]) < 0 or int(tokenized[0]) >= n: return False
        if int(tokenized[1]) < 0 or int(tokenized[1]) >= n: return False
        return True
        
    elif len(tokenized) == 3: # flag move
        if not tokenized[0] == 'flag': return False
        if not tokenized[1].isnumeric() or not tokenized[2].isnumeric(): return False
        if int(tokenized[1]) < 0 or int(tokenized[1]) >= n: return False
        if int(tokenized[2]) < 0 or int(tokenized[2]) >= n: return False
        return True
        
    return False

'''
function: main
----------
This function handles user input, translating valid moves into moves on the
board.
'''
def main(n, num_mines):
    while n > 32: # board will be too big for recursion
        print('Please enter a new board size smaller than 32:', end=' ')
        newN = input()
        if newN.isnumeric():
            n = int(newN)
        
    while n ** 2 - 1 < num_mines: # there are too many mines to place on the board
        print(f'Please enter a new number of mines smaller than {(n ** 2)}', end=' ')
        newNumMines = input()
        if newNumMines.isnumeric():
            num_mines = int(newNumMines)
            
    game = Board(n, num_mines, verbose=True)
    
    while True:
        # get user input for next move
        print('--->', end=' ')
        userInput = input()
        
        # quit game
        if userInput == 'q': break
        
        elif not isValidInput(userInput, n):
            print('Please enter a valid input')
            continue
            
        else:
            # flag move
            if userInput.split(' ')[0] == 'flag':
                game.flag(int(userInput.split(' ')[1]), int(userInput.split(' ')[2]))
            
            # regular move
            else:
                game.move(tuple([int(i) for i in userInput.split(' ')]))
                if game.lost or game.won:
                    break

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', nargs='?', type=int, default=10)
    parser.add_argument('num_mines', nargs='?', type=int, default=10)
    return parser.parse_args() 

if __name__ == "__main__":
    args = parse_args()
    main(args.n, args.num_mines)
