import chess
import sys

class ChessState(chess.Board):
    """
    Chess board subclass implementing the interface needed for minimax
    """
    def __init__(self, *args, evaluate=(lambda _: return 0),  **kwargs):
        self.evaluate = evaluate
        super().__init__(*args, **kwargs)

    def value(self):
        if (self.is_stalemate() or
                self.is_insufficient_material() or
                self.can_claim_draw()):
            return 0

        if self.is_checkmate():
            return float("inf" if self.turn == chess.BLACK else "-inf")

        return self.evaluate(self)

    def moves(self):
        return self.generate_legal_moves()

    def do(self, move):
        """Return a new board resulting from the current player taking move"""
        pass

    def is_terminal(self):
        return self.is_game_over()
