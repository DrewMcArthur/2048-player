class Player:
    def __init__(self, d=4):
        self.maxdepth = d
    
    def utility(self, state):
        return state.score
        # return len(state.getEmptyLocations())
    
    def choose_move(self, state):
        return self.max_decision(state)

    def max_decision(self, state):
        """ a non-terminal state --> an ideal operator """
        # all possible moves given the current state for the current player
        ops = state.getOps()
        # their corresponding values (value of each defined by util recursively)
        choices = []

        nBranches = len(ops)

        # get the vals
        for op in ops:
            # append negative value, since this will return the value for the 
            # state after the move, which gives a value for the opposite player
            v = self.maxvalue(state.apply(op), 1)
            choices.append((v, op))

        # return op with max value
        return max(choices)[1] if choices else None
    
    def maxvalue(self, state, depth):
        """ given a depth and a state, recursively return 
            the highest expected value of the state by iterating through 
            each possible move for the other player and returning 
            the smallest value for each of those.  """
        # we always want to avoid an end game, so gameover is -infinity
        if state.gameover():
            return -float('inf')
        # otherwise, we return the utility, which is currently score
        if depth > self.maxdepth:
            return self.utility(state)

        ops = state.getOps()
        m = -float('inf')

        # recursively find the highest value state.  negatives included because
        # maxvalue(otherplayer) will return their best value, which is opposite
        # from what we want.
        for op in ops:
            # get a new state for the opposite player from that op
            result = state.apply(op)

            # and get the value of their most likely move
            # that's negative for us, then we want to maximize that.
            v = self.maxvalue(result, depth + 1)

            # m keeps track of the max value
            m = max(m, v)

        # return the highest value for the given state
        return m
