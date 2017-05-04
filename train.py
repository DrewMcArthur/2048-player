"""
    trains the neural net, main plays one game with minimax player
    while the neural net watches and learns.  
    one move is one iteration of training
"""

from game import Board, Piece
from player import Player
from nn_player import nn_player
from getch import getch
from tqdm import tqdm

def save_num_iters():
    f = open('num_iters.pysave', 'rw+')
    n = int(f.read(1))
    if n:
        f.write(str(n+1))
    else:
        f.write("1")
    f.close

def main():
    # create a game, and two players. 
    b = Board()
    p = Player(4)           # minimax player
    nnp = nn_player()       # neural net player
    while not b.gameover():
        move = p.choose_move(b)     # get a move using minimax
        nnp.correct_move(b, move)   # train the neural net with that move
        b = b.apply(move)           # play the move

    nnp.save_net()                  # after each game, save the neural net
    print()                         # then print out the board and score
    b.printBoard()
    print()
    print("Score:",b.score)
    print()
    print("Wow, good game!")

if __name__ == "__main__":
    # play 1000 games
    [main() for _ in tqdm(range(1000))]
