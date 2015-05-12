class MinimaxState(object):
    """
    Abstract base class of game states suitabe for minimax.

    Games that fit this model have two players, and a set of terminal states
    with well-defined values. One player tries to minimize the final value
    (min), and one tries to maximize it (max). The game state includes the
    player whose turn it is. Each nonterminal state has a set of moves that can
    be taken by the player whose turn it is, and each move deterministically
    results in a new game state.
    """
    def __init__(self):
        raise NotImplementedError

    def value(self):
        """
        Get the value of a state.
        
        Returns the final score corresponding to this state if it's terminal,
        or a heuristic estimate if not.
        """
        raise NotImplementedError 

    def moves(self):
        raise NotImplementedError

    def do(self, move):
        raise NotImplementedError

    def is_terminal(self):
        raise NotImplementedError

MAX = 1
MIN = -1

def minimax(state, player=MAX, maxdepth=-1):
    """
    Return a (value, move) tuple representing the action taken by player.
    """
    better = max if player == MAX else min
    results = []
    for move in state.moves():
        result = state.do(move)
        if maxdepth != 0 or result.is_terminal():
            results.append((result.value(), move))
        else:
            value = minimax(result, player=(-player), maxdepth=(maxdepth - 1))[0]
            results.append((value, move))


    best = better(results, key=(lambda a: a[0]))
    return best
