import chess
import chess_state

def evaluate_material(board, q=9, r=5, b=3, n=3, p=1):
    acc = 0
    values = {
            chess.PAWN: p,
            chess.KNIGHT: n,
            chess.BISHOP: b,
            chess.ROOK: r,
            chess.QUEEN: q,
            }
    for i in range(64):
        piece = board.piece_at(i)

        if not piece:
            continue

        if piece.color == chess.WHITE:
            acc += values.get(piece.piece_type, 0)
        else:
            acc -= values.get(piece.piece_type, 0)

    return acc

class compound_evaluate(object):
    def __init__(self, evaluator_pairs=None):
        self.evaluators = evaluators or [(1, evaluate_material)]

    def __call__(self, board):
        acc = 0
        for weight, evaluator in self.evaluators:
            acc += weight * evaluator(board)
        return acc
