import chess
import sys

class ChessState(chess.Board):
    """
    Chess board subclass implementing the interface needed for minimax
    """
    def __init__(self, evaluate=(lambda _: 0),  fen=None):
        self.evaluate = evaluate
        super().__init__(fen=fen)

    def __str__(self):
        result = []
        for i in range(8):
            line = []
            for j in range(8):
                piece = self.piece_at(8*i+j)
                if piece:
                    line.append(piece.symbol())
                else:
                    line.append('#')
            result.append(''.join(line))
        return '\n'.join(reversed(result))


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
        result = ChessState(evaluate=self.evaluate, fen=self.fen())
        result.push(move)
        return result

    def is_terminal(self):
        return self.is_game_over()
