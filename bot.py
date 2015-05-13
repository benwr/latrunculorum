import argparse
import chess
import sys

import chess_state
import evaluators
import minimax

import time

argparser = argparse.ArgumentParser()
argparser.add_argument('--player', "-p", default="white", type=str, help="'[w]hite' or '[b]lack'; the bot player's color")

class Bot(object):
    """
    Implements one player of the game.
    """
    def __init__(
            self,
            player=chess.WHITE,
            searchdepth=5,
            evaluate=evaluators.MaterialEvaluator(),
            transposition_tables=True):
        self.state = chess_state.ChessState(
                evaluate=evaluate,
                memoize=transposition_tables)
        self.player = player
        self.searchdepth = searchdepth
        self.wins = 0
        self.loses = 0
        self.stalemates = 0

    def reset_game(self):
        self.state.reset()
        self.player = chess.WHITE
        
    def choose_move(self):
        """Given the current board state, choose a best move."""
        value, move = minimax.alphabeta(self.state,
                player=(minimax.MAX
                    if self.player == chess.WHITE
                    else minimax.MIN),
                maxdepth=self.searchdepth)

        return value, move

    def make_move(self, move):
        """Modify the board state by making the given move."""
        if (self.state.piece_type_at(move.from_square) == chess.PAWN or
                self.state.piece_at(move.to_square)):
            self.state.values = dict()
        self.state.push(move)


class Supervisor():
    bots = []
    def __init__(self, number):
        for i in range(0, number):
            self.bots.append(Bot())

    def begin(self):
        print("starting bot moves")

        while True:
            for bot in self.bots:
                print(bot)
                for other_bot in self.bots:
                    print(other_bot)
                    m1 = bot.choose_move()
                    bot.make_move(m1)
                    m2 = other_bot.choose_move()
                    other_bot.make_move(m2)
                    print(other_bot.state)
                    if bot.state.is_game_over() or other_bot.state.is_game_over():
                        print("game over!")
                        bot.reset_game()
                        other_bot.reset_game()
                        
                        break

def main():
    supervisor = Supervisor(3)
    supervisor.begin()

    
def main1(player=chess.WHITE, searchdepth=5):
    b = Bot(player=player, searchdepth=searchdepth)
    if player == chess.WHITE:
        # if the bot is white, make a first move.
        value, m = b.choose_move()
        print(value)
        print(m.uci())
        b.make_move(m)
        print(b.state)
        print()

    while True:
        # take a move as input
        try:
            m = chess.Move.from_uci(input())
        except ValueError:
            m = chess.Move.from_uci('a1a1')

        # verify that it's a possible move
        while not b.state.is_legal(m):
            print("Illegal move! Try again.\n")
            m = chess.Move.from_uci(input())
 
        # make the move
        b.make_move(m)
        print(b.state)
        print()
        if b.state.is_game_over():
            print("Game over!")
            break

        # Choose and make a move of our own.
        value, m = b.choose_move()
        print(value)
        print(m.uci())
        b.make_move(m)
        print(b.state)
        print()

        if b.state.is_game_over():
            print("Game over!")
            break

if __name__ == "__main__":
    args = argparser.parse_args()
    main1()

