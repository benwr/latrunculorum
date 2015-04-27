import chess
import chess_state

def evaluate_material(board, q=9, r=5, b=3, n=3, p=1):
    acc = 0
    acc += p * (len(board.pieces(chess.PAWN, chess.WHITE)) -
            len(board.pieces(chess.PAWN, chess.BLACK)))
    acc += n * (len(board.pieces(chess.KNIGHT, chess.WHITE)) -
            len(board.pieces(chess.KNIGHT, chess.BLACK)))
    acc += b * (len(board.pieces(chess.BISHOP, chess.WHITE)) -
            len(board.pieces(chess.BISHOP, chess.BLACK)))
    acc += r * (len(board.pieces(chess.ROOK, chess.WHITE)) -
            len(board.pieces(chess.ROOK, chess.BLACK)))
    acc += q * (len(board.pieces(chess.QUEEN, chess.WHITE)) -
            len(board.pieces(chess.QUEEN, chess.BLACK)))

    return acc

class compound_evaluate(object):
    def __init__(self, evaluator_pairs=None):
        self.evaluators = evaluators or [(1, evaluate_material)]

    def __call__(self, board):
        acc = 0
        for weight, evaluator in self.evaluators:
            acc += weight * evaluator(board)
        return acc
