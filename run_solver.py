import argparse, time
from solver import solve
from board import Board

def run_solver(n, num_mines, num_trials, animate):
    wins = 0
    start_time = time.time()
    for i in range(num_trials):
        board = Board(n, num_mines)
        if solve(board, animate):
            wins += 1

        current_percentage = (i + 1) * 100 // num_trials
        print(f'\r{current_percentage}% complete ({i+1}/{num_trials})', end='')

    finish_time = time.time()
    print()
    print(f'Time taken: {finish_time - start_time:.2f}s')
    print(f'Win percentage: {wins * 100 / num_trials:.2f}% ({wins}/{num_trials})')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', nargs='?', type=int, default=10)
    parser.add_argument('num_mines', nargs='?', type=int, default=10)
    parser.add_argument('num_trials', nargs='?', type=int, default=100000)
    parser.add_argument('-a', '--animate', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run_solver(args.n, args.num_mines, args.num_trials, args.animate)    