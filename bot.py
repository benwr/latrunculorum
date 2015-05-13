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
    def __init__(self, player=chess.WHITE, searchdepth=5, evaluate=evaluators.MaterialEvaluator()):
        self.state = chess_state.ChessState(evaluate=evaluate)
        self.player = player
        self.searchdepth = searchdepth
        self.wins = 0
        self.loses = 0
        self.stalemates = 0

    def reset_game(self):
        chess_state.ChessState().reset()
        self.state = chess_state.ChessState(evaluators.MaterialEvaluator())
        self.player = chess.WHITE
        self.searchdepth = 5
        self.wins = 0
        self.loses = 0
        self.stalemates = 0
        
    def choose_move(self):
        """Given the current board state, choose a best move."""
        _, move = minimax.minimax(self.state,
                player=(minimax.MAX
                    if self.player == chess.WHITE
                    else minimax.MIN),
                maxdepth=self.searchdepth)

        return move

    def make_move(self, move):
        """Modify the board state by making the given move."""
        self.state.push(move)


class Supervisor():
    bots = []
    def __init__(self, number):
#        self.bots = []
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

#        while True:
#            m1 = self.bot1.choose_move()
#            self.bot1.make_move(m1)
#            m2 = self.bot2.choose_move()
#            self.bot2.make_move(m2)

#            print(self.bot2.state)

#            if self.bot1.state.is_game_over() or self.bot2.state.is_game_over():
#               print("game over!")
#                break
            
            #time.sleep(2)

def main():
    supervisor = Supervisor(3)
    supervisor.begin()

    
def main1(player=chess.WHITE, searchdepth=2):
    b = Bot(player=player, searchdepth=searchdepth)
    if player == chess.WHITE:
        # if the bot is white, make a first move.
        m = b.choose_move()
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
        m = b.choose_move()
        print(m.uci())
        b.make_move(m)
        print(b.state)
        print()

        if b.state.is_game_over():
            print("Game over!")
            break

if __name__ == "__main__":
    args = argparser.parse_args()
    main()

