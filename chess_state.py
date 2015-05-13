import chess
import sys

class ChessState(chess.Board):
    """
    Chessboard subclass implementing the interface needed for minimax
    """
    def __init__(self, evaluate=(lambda _: 0),  fen=None):
        # evaluate is an heuristic function taking a board state
        # and returning an approximate value.
        self.evaluate = evaluate
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


    def value(self):
        """Get ground value of state, if exists, or evaluate(state) if not."""

        winner = self.winner()
        if winner == False:
            return self.evaluate(self)

        # draws are neutral
        if winner is None:
            return 0

        # Good for winner, bad for loser
        return float("inf" if winner == chess.BLACK else "-inf")

    def moves(self):
        return self.generate_legal_moves()

    def do(self, move):
        """Return a new board resulting from the current player taking move"""
        result = ChessState(evaluate=self.evaluate, fen=self.fen())
        result.push(move)
        return result

    def is_terminal(self):
        return self.is_game_over()
