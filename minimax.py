import random

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
    for move, result in state.moves():
        # result = state.do(move)
        if maxdepth == 0 or result.is_terminal():
            results.append((result.value(), move))
        else:
            value = minimax(result, player=(-player), maxdepth=(maxdepth - 1))[0]
            results.append((value, move))

    random.shuffle(results)
    best = better(results, key=(lambda a: a[0]))
    return best

def max_value(state, alpha, beta, depth):
    if state.is_terminal() or depth == 0:
        return (None, state.value())

    v = float("-inf")
    best = None

    for move in state.generate_legal_moves():
        state.push(move)
        _, result = min_value(state, alpha, beta, depth=(depth-1))
        if result is not None and v < result:
            v = result
            best = move
        state.pop()
        if v >= beta:
            return (move, v)
        alpha = max(alpha, v)

    return (best, v)

def min_value(state, alpha, beta, depth):
    if state.is_terminal() or depth == 0:
        return (None, state.value())

    v = float("inf")
    best = None

    for move in state.generate_legal_moves():
        state.push(move)
        _, result = max_value(state, alpha, beta, depth=(depth-1))
        if result is not None and v > result:
            v = result
            best = move
        state.pop()
        if v <= alpha:
            return (move, v)
        beta = min(beta, v)

    return (best, v)

def alphabeta(state, player=MAX, maxdepth=6):
    if player == MAX:
        v, move = max_value(state, float("-inf"), float("inf"), maxdepth)
    else:
        v, move = min_value(state, float("-inf"), float("inf"), maxdepth)
    return move, v
