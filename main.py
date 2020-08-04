from games import *
import time
import random
import math
import hashlib
import logging
import argparse
from mcts import *


initial_state = {'P': True, 'Q': False, 'R': True, 'S': False, 'T': True, 'U': False, 'V': True, 'W': False, 'X': True, 'Y': False,
                 'P11': True, 'Q11': False,'R11': True, 'S11': False, 'T11': True, 'U11': False,'V11': True, 'W11': False,'X11': True, 'Y11': False,
                 'P22': True, 'Q22': False, 'R22': True, 'S22': False}

start_time = time.time()

#minimax_decision(initial_state,gameofgoals)

#expectiminimax(initial_state,gameofgoals)

#alphabeta_cutoff_search(initial_state,gameofgoals,30)

#print("--- %s seconds ---" % (time.time() - start_time))

#===========================================================
#==================MCTS==========================
#===========================================================

NUM_TURNS = 5


class AntasState():
    def __init__(self, current=[0] * 2 * NUM_TURNS, turn=0):
        self.current = current
        self.turn = turn
        self.num_moves = (114 - self.turn) * (114 - self.turn - 1)

    def next_state(self):
        availableActions = [x for x in range(1, 115)]
        for c in self.current:
            if c in availableActions:
                availableActions.remove(c)
        player1action = random.choice(availableActions)
        availableActions.remove(player1action)
        nextcurrent = self.current[:]
        nextcurrent[self.turn] = player1action
        player2action = random.choice(availableActions)
        availableActions.remove(player2action)
        nextcurrent[self.turn + NUM_TURNS] = player2action
        next = AntasState(current=nextcurrent, turn=self.turn + 1)
        return next

    def terminal(self):
        if self.turn == NUM_TURNS:
            return True
        return False

    def reward(self):
        r = random.uniform(0, 1)  # ANTAS, put your own function here
        return r

    def __hash__(self):
        return int(hashlib.md5(str(self.current).encode('utf-8')).hexdigest(), 16)

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

    def __repr__(self):
        s = "CurrentState: %s; turn %d" % (self.current, self.turn)
        return s

if __name__ == "__main__":
    num_sims = 13000

    #parser = argparse.ArgumentParser(description='MCTS research code')
    #parser.add_argument('--num_sims', action="store", required=True, type=int,
    #                    help="Number of simulations to run, should be more than 114*113")
    #args = parser.parse_args()

    current_node = Node(AntasState())

    start_time = time.time()

    # minimax_decision(initial_state,gameofgoals)

    # expectiminimax(initial_state,gameofgoals)

    # alphabeta_cutoff_search(initial_state,gameofgoals,30)

    for l in range(NUM_TURNS):
        current_node = UCTSEARCH(num_sims / (l + 1), current_node)
        print("level %d" % l)
        print("Num Children: %d" % len(current_node.children))
        for i, c in enumerate(current_node.children):
            print(i, c)
        print("Best Child: %s" % current_node.state)
        print("--------------------------------")

    print("--- %s seconds ---" % (time.time() - start_time))

