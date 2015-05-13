import chess
import sys

class ChessState(chess.Board):
    """
    Chessboard subclass implementing the interface needed for minimax
    """
    def __init__(self, evaluate=(lambda _: 0), memoize=False,  fen=None):
        # evaluate is an heuristic function taking a board state
        # and returning an approximate value.
        self.evaluate = evaluate
        self.memoize = memoize
        if memoize:
            self.values = dict()
        super().__init__(fen=fen)

    def __str__(self):
        # Board representation
        result = ['  ABCDEFGH']
        for i in range(8):
            line = [str(i+1), ' ']
            for j in range(8):
                piece = self.piece_at(8*i+j)
                if piece:
                    line.append(piece.symbol())
                else:
                    line.append('#')
            result.append(''.join(line))
        return '\n'.join(reversed(result))

    def winner(self):
        if (self.is_stalemate() or
                self.is_insufficient_material() or
                self.can_claim_draw()):
            return None

        if not self.is_game_over():
            return False

        return chess.WHITE if self.turn == chess.BLACK else chess.BLACK

    def hashable(self):
        return (self.occupied_co[chess.WHITE],
                self.occupied_co[chess.BLACK],
                self.pawns,
                self.knights,
                self.bishops,
                self.rooks,
                self.queens,
                self.kings)

    def value(self):
        """Get ground value of state, if exists, or evaluate(state) if not."""
        h = self.hashable()

        if self.memoize and h in self.values:
            return self.values[h]

        result = None

        winner = self.winner()

        if winner == False:
            # Game's not over
            result = self.evaluate(self)
        elif winner is None:
            # Draws are neutral
            result = 0
        else:
            # Good for winner, bad for loser
            result = float("inf" if winner == chess.BLACK else "-inf")

        if self.memoize:
            self.values[h] = result
            
        return result

    def moves(self):
        for move in self.generate_legal_moves():
            self.push(move)
            yield (move, self)
            self.pop()

    def do(self, move):
        """Return a new board resulting from the current player taking move"""
        result = ChessState(evaluate=self.evaluate, fen=self.fen(), memoize=self.memoize)
        result.push(move)
        return result

    def is_terminal(self):
        return self.is_game_over()
