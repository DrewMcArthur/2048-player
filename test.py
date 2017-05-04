from game import Board, Piece
from player import Player
from nn_player import nn_player
from getch import getch
from tqdm import tqdm

def main():
    b = Board()
    p = Player(4)
    nnp = nn_player()
    while not b.gameover():
        #print()
        #b.printBoard()
        #print()
        #print("Score:",b.score)
        #print()
        move = p.choose_move(b)
        nnp.correct_move(b, move)
        b = b.apply(move)

    nnp.save_net()
    print()
    b.printBoard()
    print()
    print("Score:",b.score)
    print()
    print("Wow, good game!")

if __name__ == "__main__":
    [main() for _ in tqdm(range(100))]
