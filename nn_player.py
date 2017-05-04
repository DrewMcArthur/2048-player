from player import Player
from nn import NN
import signal
import sys
import os

class nn_player(Player):
    def __init__(self):
        self.maxdepth = 4
        self.moves = ["up", "right", "down", "left"]
        self.nn = NN([16,4])

        self.weightFile = open("2048_nn_weights.pysave", "wb+")
        if os.stat("2048_nn_weights.pysave").st_size > 0:
            self.nn.loadWeights(self.weightFile)

        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        """ saves the weights for the neural net before exiting. """
        print("Saving weights and exiting process...")
        self.save_net()
        sys.exit(0)

    def save_net(self):
        """ saves the weights for the neural net in the file specified
            in __init__ """
        self.nn.saveWeights(self.weightFile)

    def choose_move(self, state):
        """ given a board, returns the neural net's choice move """

        # get a list of normalized inputs that represents the board
        d = self.normalize_grid(state)
        # input that into the neural net
        self.nn.forward_propagate(d)

        # get the output, in the form of an index of which output was highest
        # e.g. [0.23, 0.49, 0.85, 0.17] => 2
        o = self.nn.get_discrete_output()
        # return the string move associated with that index
        return self.moves[o]

    def correct_move(self, state, move):
        """ gives the player a state and a "correct" move, 
            essentially one iteration of training the neural net."""

        # get a list of normalized inputs that represents the board
        d = self.normalize_grid(state)
        # input that into the neural net
        self.nn.forward_propagate(d)

        # use the move to create a proper output list
        l = [0 for _ in range(4)]
        l[self.moves.index(move)] = 1

        # use a learning rate proportional to the game's score
        alpha = state.score / 100000
        # and correct the neural net.
        self.nn.backward_propagate(l, alpha) 

    def normalize(self, u, mn, mx):
        """ given a value [u], minimum and maximum, return a value 0 to 1 """
        return (u - mn) / (mx - mn)

    def normalize_grid(self, state):
        """ given a state, return a list of the pieces, normalized. """

        # get a list of all the values of the pieces
        data = []
        for row in state.pieces:
            [data.append(piece) for piece in row]

        # set the min and max values
        mn = 0
        mx = max([d.val for d in data])

        # normalize input data
        for i in range(len(data)):
            data[i] = self.normalize(data[i].val, mn, mx)

        return data
