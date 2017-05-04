# nn.py

import sys
import math
import pickle
import random

class NN:
    def __init__(self, nodesInLayer):
        if 0 in nodesInLayer:
            nodesInLayer.remove(0)

        # a list: the number of nodes in each layer:
        self._numLayers = len(nodesInLayer)
        self._nodesInLayer = nodesInLayer
        
        # a list: for each layer l except 0, an i x j matrix of weights 
        # from node i in previous layer to node j in this layer.
        # thus:  self._weights[l][i][j] is a weight on a connection in the
        # network.
        # n.b. index l==0 is not used
        self._weights = [None]  # None holds place 0.
        for layer in range(1, self._numLayers):
            self._weights.append(makeMatrix(nodesInLayer[layer-1], 
                                            nodesInLayer[layer]))
        
        # self._in: a 2D list.  self._in[l][j] is the weighted sum of inputs
        # from all nodes i in layer l-1 to node j in layer l.
        #  n.b. index l==0 is not used.
        self._in = [[0] * nodesInLayer[i] for i in range(self._numLayers)]

        # activations:  the outputs from each node in the network..
        # self._activations[l][i] is the activation of node i in layer l.
        self._activations = [[0] * self._nodesInLayer[i] 
                             for i in range(self._numLayers)]

        # self._deltas: a 2D list.  One delta for each node 
        # except those in the first layer.
        # self._deltas[l][i] for l > 0.
        self._deltas = [[0] * nodesInLayer[i] for i in range(self._numLayers)]


    def loadWeights(self, fileHandle):
        """ POST: filehandle points to a pickled nested list """
        self._weights = pickle.load(fileHandle)

    def saveWeights(self, fileHandle):
        """ PRE: filehandle points to a pickled nested list """
        pickle.dump(self._weights, fileHandle)

    def forward_propagate(self, inputs):
        # give values to input nodes
        assert len(inputs) == self._nodesInLayer[0]
        for i in range(len(inputs)):
            self._activations[0][i] = inputs[i]
        for l in range(1, self._numLayers):
            for j in range(self._nodesInLayer[l]):
                self._in[l][j] = \
                    sum([self._weights[l][i][j] * self._activations[l-1][i] 
                         for i in range(self._nodesInLayer[l-1])])
                self._activations[l][j] = sigma(self._in[l][j])

    def backward_propagate(self, t_values, alpha):
        """ Given a list of desired activations on the last layer
            do a backpropogate and update the weights on the network.
            PRE:  forward_propagate has been done with inputs, and
                  t_values are the desired output for those inputs.  """

        L = self._numLayers
        for j in range(self._nodesInLayer[L - 1]):
            # set the delta to the output of sigma prime times the difference
            # between the NN output and the actual output
            self._deltas[L-1][j] = sigma_p(self._in[L-1][j]) * \
                                    (t_values[j] - self._activations[L-1][j])
        # iterate backwards from last layer to first hidden layer
        for l in range(self._numLayers - 2, 0, -1):
            # within each layer, iterate through each node
            for i in range(self._nodesInLayer[l]):
                # delta for this node is equal to:
                #   g'(input) * sum(weights * deltas 
                #                       foreach node in next layer)
                self._deltas[l][i] = sigma_p(self._in[l][i]) * \
                            sum([self._weights[l+1][i][j] * self._deltas[l+1][j]
                            for j in range(self._nodesInLayer[l+1])])

        for l in range(1, self._numLayers):
            for i in range(self._nodesInLayer[l-1]):
                for j in range(self._nodesInLayer[l]):
                    # adjust each weight by 
                    # alpha * activations in the last layer * delta at this node
                    self._weights[l][i][j] += (alpha * self._activations[l-1][i]
                                                     * self._deltas[l][j])

    def get_error(self, t_values):
        """ return error as sum of squares of differences between desired 
            output (t_values) and corresponding activations on output 
            nodes """
        assert len(t_values) == self._nodesInLayer[self._numLayers-1]
        return sum([(t_values[i] - self._activations[self._numLayers-1][i]) 
                     ** 2 
                    for i in range(len(t_values))])

    def get_output(self):
        """ Return a copy of the activations of the last layer """
        return list(self._activations[self._numLayers-1])

    def get_discrete_output(self):
        """ returns the index of the output that had the highest activation."""
        o = self.get_output()
        return o.index(max(o))

    def print(self):
        print("{}, a NN with {} layers".format(self, self._numLayers))
        for l in range(self._numLayers):
            if l > 0:
                print("Weights from layer {} to layer {}".format(l-1, l))
                for j in range(self._nodesInLayer[l]):
                    print(" To node {} in layer {}".format(j, l))
                    for i in range(self._nodesInLayer[l-1]):
                        print("  " + str(self._weights[l][i][j]) + " ")
                    print()
            print("Activations at layer {}".format(l))
            print(self._activations[l])
            print()
        print("================================")
            
def makeMatrix(rows, cols):
    """ return a random matrix """
    return [[random.random() for _ in range(cols)] for _ in range(rows)]  

def sigma(x):
    # sigmoid function
    return 1 / (1 + math.e ** -x)

def sigma_p(x):
    # derivative of sigmoid function
    return (math.e ** -x) / (1 + math.e ** -x) ** 2

