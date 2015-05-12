import chess
import chess_state

class MaterialEvaluator(object):
    def __init__(self, q=9, r=5, b=3, n=3, p=1, memoize=True):
        self.q, self.r, self.b, self.n, self.p = q, r, b, n, p
        self.memoize = memoize
        if memoize:
            self.results= dict()
        self.values = {
                chess.PAWN: p,
                chess.KNIGHT: n,
                chess.BISHOP: b,
                chess.ROOK: r,
                chess.QUEEN: q,
                }

    def __call__(self, board):
        if self.memoize:
            tup = (board.pawns, board.knights, board.bishops, board.rooks, board.queens, board.kings)
            result = self.results.get(tup, None)
            if result is not None: return result

        acc = 0
        for i in range(64):
            piece = board.piece_at(i)

            if not piece:
                continue

            if piece.color == chess.WHITE:
                acc += self.values.get(piece.piece_type, 0)
            else:
                acc -= self.values.get(piece.piece_type, 0)
        
        if self.memoize: self.results[tup] = acc

        return acc

class CompoundEvaluate(object):
    def __init__(self, evaluator_pairs=None):
        self.evaluators = evaluator_pairs or [(1, MaterialEvaluator())]

    def __call__(self, board):
        acc = 0
        for weight, evaluator in self.evaluators:
            acc += weight * evaluator(board, memoize=False)
        return acc
