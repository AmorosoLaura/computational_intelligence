import random
from game import Game, Move, Player
from copy import deepcopy
import collections
import sys


class RandomPlayer(Player):
    """class defining a player that chooses his moves randomly"""
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

""" 
class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()


    def get_legal_moves(self, game):
        legal_moves = []
        for i in range(5):
            for j in range(5):
                if game.get_board()[i][j] == -1:

                    legal_moves.append((i, j))
        return legal_moves
    
    def minmax(self, game, depth, maximizing_player):

        if depth == 0 or game.check_winner()!=-1:
            # Return the heuristic value for the current board state
            #return evaluate_board(board)
            return game.check_winner()
        legal_moves = self.get_legal_moves(game)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = game.get_board()
                new_board.make_move(move, 'O')
                eval = self.minmax(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = game.get_board()
                new_board.make_move(move, 'X')
                eval = self.minmax(new_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
         
        legal_moves = self.get_legal_moves(game)

        best_move = None
        best_eval = float('-inf')

        for move in legal_moves:
            new_board = game.get_board()
            new_board.make_move(move, 'O')
            eval = self.minmax(new_board, 2, False)  # Adjust the depth as needed
            if eval > best_eval:
                best_eval = eval
                best_move = move 
        return best_move 
         """

class MinmaxPlayer(Player):
    def make_move(self, game: 'QuixoGame') -> tuple[tuple[int, int], Move]:
        return self.minmax(game, 3)


    def get_legal_moves(self, game):
        legal_moves = []
        for i in range(5):
            for j in range(5):
                if game.get_board()[i][j] == -1:

                    legal_moves.append((i, j))
        return legal_moves
    
    def minmax(self, game, depth):
        legal_moves = self.get_legal_moves(game)

        maximizing_player = game.get_current_player() == 1  # Assuming player 1 is the maximizing player

        best_eval = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in legal_moves:
            new_game = deepcopy(game)
            new_game.__move(move, 'O')  # Assuming 'O' represents the player using Minimax
            eval = self.minmax_recursive(new_game, depth-1, float('-inf'), float('inf'), not maximizing_player)

            if maximizing_player and eval > best_eval:
                best_eval = eval
                best_move = move
            elif not maximizing_player and eval < best_eval:
                best_eval = eval
                best_move = move

        return best_move

    def minmax_recursive(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_winner() >= 0:
            return self.evaluate_board(game)

        legal_moves = game.get_legal_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_game = deepcopy(game)
                new_game.__move(move, 'O')
                eval = self.minmax_recursive(new_game, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_game = deepcopy(game)
                new_game.make_move(move, 'X')  # Assuming 'X' represents the opponent
                eval = self.minmax_recursive(new_game, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, game):
        # Your evaluation function goes here
        # This function should return a numerical value indicating the desirability of the current game state for the maximizing player
        pass

def get_all_possible_moves(game: Game) -> list[tuple[tuple[int, int], Move]]:
    """
    Returns a list of all possible moves from the current board state.
    """
    possible_moves = []

    # Get the board
    board = game.get_board()

    # Make a copy of the board to work with
    game = deepcopy(game)

    # For each row and column
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            # Get the piece at the current position
            piece = board[row, col]

            # Only consider unconquered and non-neutral pieces
            if piece < -1 or piece > 1:
                continue

            # For each possible move
            for slide in Move:
                #print(slide)
                # Only consider valid moves
                acceptable = game.move((row, col), slide, piece)
                if acceptable:
                    # Add the move to the list of possible moves
                    possible_moves.append(((row, col), slide))

    return possible_moves


def evaluate_board(game: Game) -> float:
    # Get the board
    board = game.get_board()

    # Get the number of conquered pieces for each player
    conquered_pieces = {p: 0 for p in range(2)}
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row, col] != -1 and board[row, col] != 0:
                conquered_pieces[board[row, col]] += 1

    # Get the number of pieces lined up for each player
    pieces_in_a_row = {p: 0 for p in range(2)}
    for direction in Move:
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col] != -1:
                    connected_pieces = _check_connected_pieces(game, (row, col), direction)
                    if len(connected_pieces) > pieces_in_a_row[board[row, col]]:
                        pieces_in_a_row[board[row, col]] = len(connected_pieces)

    # Get the number of pieces that can be captured for each player
    capturable_pieces = {p: 0 for p in range(2)}
    for row in range(board.shape[0] - 1):
        for col in range(board.shape[1] - 1):
            if board[row, col] != -1:
                for slide in Move:
                    if game.can_move((row, col), slide):
                        capturable_pieces[board[row, col]] += 1

    # Combine the scores for each metric
    score = 2 * conquered_pieces[1] - conquered_pieces[0]
    score += 3 * pieces_in_a_row[1] - pieces_in_a_row[0]
    score += 3 * capturable_pieces[1] - capturable_pieces[0]
    return score


class MinMaxPlayer:
    """ sssssssssssssssssssss"""
    def __init__(self, depth=5):
        self.depth = depth
        self._opponent = RandomPlayer()

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """ sssssssssssssssssssss"""
        # Get all possible moves from the current board state
        possible_moves = get_all_possible_moves(game)
        print(possible_moves)
        # Initialize alpha and beta
        alpha = float('-inf')
        beta = float('inf')

        # Evaluate all possible moves using minimax with alpha-beta pruning
        best_move = None
        for from_pos, slide in possible_moves:
            print(from_pos, slide)
            evaluation = self.minmax(game, from_pos, slide, depth=self.depth, alpha=alpha, beta=beta)

            if evaluation > alpha:
                alpha = evaluation
                best_move = (from_pos, slide)

        return best_move

    def minmax(self, game: Game, from_pos: tuple[int, int], slide: Move, depth: int, alpha: float, beta: float) -> float:
        """
        Calculates the maximum utility for a move using minimax with alpha-beta pruning.

        Args:
            game: The current game state.
            from_pos: The starting position of the move.
            slide: The direction of the move.
            depth: The current depth in the search tree.
            alpha: The current lower bound of the maximum utility.
            beta: The current upper bound of the maximum utility.

        Returns:
            The maximum utility for the move.
        """

        # If we have reached the maximum depth, evaluate the current board state
        if depth == 0:
            return evaluate_board(game)

        # Get the potential next board states if we make the current move
        next_games = [deepcopy(game) for _ in range(len(game.get_board()))]

        # For each potential next board state, evaluate the utility of the child state using minmax
        for next_game in next_games:
            next_game.play(self._opponent, self)
            opponent_evaluation = self.minmax(next_game, from_pos, slide, depth - 1, -beta, -alpha)

            # Update alpha and best move
            if self.is_maximizer(next_game):
                if opponent_evaluation > alpha:
                    alpha = opponent_evaluation

                # Alpha-beta pruning
                if alpha >= beta:
                    break
            else:
                if opponent_evaluation < beta:
                    beta = opponent_evaluation

        return alpha


    def is_maximizer(self, game):
        """
        Returns True if the current player is the maximizer (player 1), False otherwise (player 2).
        """
        return game.get_current_player() == 0


import numpy as np

class MyPlayer(Player):
    def __init__(self, depth):
        self.depth = depth

    def make_move(self, game):
        _, best_move = self.minimax(game, self.depth, True, float('-inf'), float('inf'))

        #print("My player is choosing ", best_move)
        return best_move

    """ def minimax(self, game, depth, maximizing_player, alpha, beta):

        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game), None

        legal_moves = self.get_legal_moves(game)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in legal_moves:
                new_game = deepcopy(game)
                new_game.move(move[0], move[1], game.current_player_idx)
                eval, _ = self.minimax(new_game, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in legal_moves:
                new_game = deepcopy(game)
                new_game.move(move[0], move[1], game.current_player_idx)
                eval, _ = self.minimax(new_game, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
    """

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
            game._board[x, y], game._board[x - 1, y] = game._board[x - 1, y], game._board[x, y]
        elif direction == Move.BOTTOM and x < game._board.shape[0] - 1:
            game._board[x, y], game._board[x + 1, y] = game._board[x + 1, y], game._board[x, y]
        elif direction == Move.LEFT and y > 0:
            game._board[x, y], game._board[x, y - 1] = game._board[x, y - 1], game._board[x, y]
        elif direction == Move.RIGHT and y < game._board.shape[1] - 1:
            game._board[x, y], game._board[x, y + 1] = game._board[x, y + 1], game._board[x, y]

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

        for x in range(game._board.shape[0]):
            for y in range(game._board.shape[1]):
                if game._board[x, y] == -1 or game._board[x, y] == 0 :
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
        if not (0 <= x < game._board.shape[0] and 0 <= y < game._board.shape[1]):
            return False
        #check if the cell is empty:
        if game._board[x, y] ==1:
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

# Example usage:
# game = Game()
# player1 = MinmaxPlayer(depth=3)
# player2 = MinmaxPlayer(depth=3)
# winner = game.play(player1, player2)
# print(f"Player {winner} wins!")

if __name__ == '__main__':

    sys.setrecursionlimit(10000)  # Increase the recursion depth to 10000

    count=0
    for i in range(100):
        g = Game()
        #g.print()
        player1 = MyPlayer(3)
        #player1 = RandomPlayer()
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        #g.print()
        if winner==0:
            count+=1

    #print(f"Winner: Player {winner}")
    print("My player won ", count/100)