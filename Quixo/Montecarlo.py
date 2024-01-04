from random import random,choice
from copy import deepcopy
from game import Player,Move, Game
from tqdm.auto import tqdm
import numpy as np

class MontecarloAgent(Player):
    """
    agent that is trained with the montecarlo algorithm of reinforcement learning
    """
    def __init__(self, symbol):
        self.q_table = {}
        self.symbol=symbol
        self._winning_games=0
        self._drawn_games=0
        self.exploration_rate=0.1
        self.rewards=[]
        self.gamma=0.9
        self.is_train=True

    def make_move(self, state, game)-> int:
        
        if self.exploration_rate>0.01:
            self.exploration_rate*=0.99
        
        if self.gamma<0.99:
            self.gamma*=1.01

        state_key = (frozenset(state[0]), frozenset(state[1]))
        available_moves=list(self.get_legal_moves(game))

        if random() < self.exploration_rate:
            # sometimes make random moves
            action = choice(available_moves)
            self.q_table[state_key] = dict.fromkeys([action], 0)
        else:
            if state_key not in self.q_table:
                self.q_table[state_key] = dict.fromkeys(available_moves, 0)
            
            #choose the action based on the q table   
            action = max(self.q_table[state_key], key=self.q_table[state_key].get)

        if action not in available_moves:
            reward=-0.1
            
        else:
            reward=0.1
            
        self.rewards.append(reward)

        if action not in available_moves:
            action=choice(list(available_moves))
            
            if state_key not in self.q_table:
                self.q_table[state_key] = dict.fromkeys([action], 0)
            return action
            
        return action

    def add_winning(self)->None:
        self._winning_games+=1
    
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
        #check if the cell is empty:
        if game.get_board()[x, y] ==1:
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

    def print_q_table(self):

        for chiave, valore in list(self.q_table.items())[:10]:
            print(f'{chiave}: {valore}')

    def update_q_table(self, trajectory, reward):
        for state,action in trajectory:
            if (frozenset(state[0]), frozenset(state[1])) in self.q_table and action in self.q_table[(frozenset(state[0]), frozenset(state[1]))]:
                #print("STATE",state)
                #for k,v in  self.q_table[(frozenset(state[0]), frozenset(state[1]))].items():
                    #print(k,v)
                self.q_table[(frozenset(state[0]), frozenset(state[1]))][action]+=0.001 * (reward -  self.q_table[(frozenset(state[0]), frozenset(state[1]))][action])

class MontecarloGame(Game):
    """
    a subclass of the game class that changes the play method to adapt to the montecarlo agent
    """
    def __move(self, from_pos, slide, index):
        return super()._Game__move(from_pos, slide, index)

    def play(self, player1: Player, player2: Player,index) -> int:
        
        trajectory=list()
        state=(set(), set())
        
        players=[player1,player2]

        while True:
            ok = False
            current_player=players[index]
            while not ok:
                from_pos, slide = current_player.make_move(state,self)
                #print(from_pos,slide)
                ok = self.__move(from_pos, slide, current_player.symbol)
            
            move=(from_pos,slide)
            #print("player ", index, move)
            #super().print()
            trajectory.append((deepcopy(state),move))
            
            for x in range(super().get_board().shape[0]): 
                for y in range(super().get_board().shape[1]):
                    if super().get_board()[x][y]==0:
                        state[0].add((x,y))
                    elif super().get_board()[x][y]==1:
                        state[1].add((x,y))
            #print(state)
            if(super().check_winner()!=-1):
                break

            index=1-index

        # i compute the final reward
            
        final_reward=self.check_winner()

        if isinstance(player1, MontecarloAgent):
            player1.update_q_table(trajectory,final_reward)
        
        print(final_reward)
        return trajectory, final_reward