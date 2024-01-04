import random
from game import Game, Move, Player
from Montecarlo import MontecarloAgent, MontecarloGame
from copy import deepcopy
import collections
import sys


class RandomPlayer(Player):
    """class defining a player that chooses his moves randomly"""
    def __init__(self,symbol:None) -> None:
        super().__init__()
        self.symbol=symbol

    def make_move(self,state:None, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class MinmaxPlayer(Player):
    """
    player that plays according to the minmax algorithm
    """
    def __init__(self, depth, symbol):
        self.depth = depth
        self.symbol=symbol

    def make_move(self, game):
        _, best_move = self.minimax(game, self.depth, True, float('-inf'), float('inf'))

        #print("My player is choosing ", best_move)
        return best_move

    def minimax(self, game, depth, maximizing_player, alpha, beta):

        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game), None

        legal_moves = self.get_legal_moves(game)
        next_states = self.calculate_next_states(game, legal_moves)
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for i, new_game in enumerate(next_states):
                eval, _ = self.minimax(new_game, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = legal_moves[i]
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break

            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for i, new_game in enumerate(next_states):
                eval, _ = self.minimax(new_game, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = legal_moves[i]
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            #print("best_move, ", best_move)
            return min_eval, best_move
        
    def calculate_next_states(self, game, legal_moves):
        next_states = []

        for move in legal_moves:
            position, direction = move
            new_game = deepcopy(game)
            self.apply_move(new_game, position, direction)
            next_states.append(new_game)

        return next_states

    def apply_move(self, game, position, direction):
        x, y = position

        if direction == Move.TOP and x > 0:
            game.get_board()[x, y], game.get_board()[x - 1, y] = game.get_board()[x - 1, y], game.get_board()[x, y]
        elif direction == Move.BOTTOM and x < game.get_board().shape[0] - 1:
            game.get_board()[x, y], game.get_board()[x + 1, y] = game.get_board()[x + 1, y], game.get_board()[x, y]
        elif direction == Move.LEFT and y > 0:
            game.get_board()[x, y], game.get_board()[x, y - 1] = game.get_board()[x, y - 1], game.get_board()[x, y]
        elif direction == Move.RIGHT and y < game.get_board().shape[1] - 1:
            game.get_board()[x, y], game.get_board()[x, y + 1] = game.get_board()[x, y + 1], game.get_board()[x, y]

    def evaluate(self, game):
        winner = game.check_winner()
        if winner == game.current_player_idx:
            return 1
        elif winner == (game.current_player_idx + 1) % 2:
            return -1
        else:
            return 0
    def get_legal_moves(self, game):
        legal_moves = []

        for x in range(game.get_board().shape[0]):
            for y in range(game.get_board().shape[1]):
                if game.get_board()[x, y] == -1 or game.get_board()[x, y] == self.symbol :
                    for direction in Move:
                        #print((x,y), direction)
                        if self.is_move_playable(game, (x, y), direction):
                            #print("back da playable")
                            legal_moves.append(((x, y), direction))
        #print(legal_moves)
        return legal_moves

    def is_move_playable(self, game, position, direction):
        x, y = position

        acceptable: bool = (
            # check if it is in the first row
            (x == 0 and y < 5)
            # check if it is in the last row
            or (x == 4 and y< 5)
            # check if it is in the first column
            or (x <5 and y ==0)
            # check if it is in the last column
            or (x <5 and y == 4)
            # and check if the piece can be moved by the current player
        ) 
        if acceptable is False:
            return False
        # Check if the move is within the bounds of the board
        if not (0 <= x < game.get_board().shape[0] and 0 <= y < game.get_board().shape[1]):
            return False

        if game.get_board()[x, y] ==1-self.symbol:
            return False
        # Check if the move is towards an empty cell
        if direction == Move.TOP and x==0:
            #print("STEP 1")
            return False
        elif direction == Move.BOTTOM and x==4:
            #print("STEP 2")
            return False
        elif direction == Move.LEFT and y == 0:
            #print("STEP 3")
            return False
        elif direction == Move.RIGHT and y == 4:
            #print("STEP 4")
            return False

        return True

if __name__ == '__main__':

    sys.setrecursionlimit(10000)  # Increase the recursion depth to 10000
    ITERATIONS=1000
    count=0
    player1=MontecarloAgent(0)

    for i in range(ITERATIONS):
        print(i)
        #g = Game()
        g=MontecarloGame()
        #g.print()
        #player1 = MinmaxPlayer(3,1)
        #player1 = RandomPlayer()

        player2 = RandomPlayer(1)
        _,winner = g.play(player1, player2,1)
        #g.print()
        if winner==0:
            count+=1

    #print(f"Winner: Player {winner}")
    print("My player won ", count/ITERATIONS)
    #player1.print_q_table()