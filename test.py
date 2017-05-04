""" use the neural net to play a game """

from game import Board, Piece
from nn_player import nn_player

def main():
    # create a game, and two players. 
    b = Board()
    nnp = nn_player()       # neural net player
    while not b.gameover():
        print()                         # then print out the board and score
        b.printBoard()
        print()
        print("Score:",b.score)
        print()
        move = nnp.choose_move(b)   # get a move using the neural net
        b = b.apply(move)           # play the move

    nnp.save_net()                  # after each game, save the neural net
    print()                         # then print out the board and score
    b.printBoard()
    print()
    print("Score:",b.score)
    print()
    print("Wow, good game!")

if __name__ == "__main__":
    main()
