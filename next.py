import time
import numpy as np
import matplotlib.pyplot as plt
from mcts import MCTS  # Assuming MCTS is implemented in mcts.py
from games import Game  # Assuming Game class is defined in games.py

# Initialize game environment
class AdversarialGame(Game):
    def __init__(self, depth_limit=5):
        self.state = self.initial_state()
        self.depth_limit = depth_limit
    
    def initial_state(self):
        return {'P': True, 'Q': False, 'R': True, 'S': False, 'T': True, 'U': False}
    
    def is_terminal(self, state, depth):
        return depth >= self.depth_limit  # Stops at depth limit
    
    def get_actions(self, state):
        return ['action1', 'action2', 'action3']  # Dummy actions
    
    def next_state(self, state, action):
        new_state = state.copy()
        for key in new_state:
            new_state[key] = not new_state[key]  # Flip values randomly
        return new_state
    
    def evaluate(self, state):
        return sum(state.values())  # Sum of True values as utility

# Experiment setup
def run_experiment():
    depths = np.arange(2, 26, 2)
    minimax_times, mcts_times = [], []
    
    for depth in depths:
        game = AdversarialGame(depth)
        
        # Minimax Execution
        start = time.time()
        # Assuming minimax function exists (pseudo-code)
        # minimax_decision(game.initial_state())
        minimax_times.append(time.time() - start)
        
        # MCTS Execution
        start = time.time()
        mcts = MCTS()
        mcts.search(game, game.initial_state(), 100)  # Assuming 100 simulations
        mcts_times.append(time.time() - start)
    
    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(depths, minimax_times, label='Minimax with Alpha-Beta', marker='o', linestyle='-', color='black')
    plt.plot(depths, mcts_times, label='Monte Carlo Tree Search (MCTS)', marker='s', linestyle='--', color='gray')
    plt.xlabel('Search Depth Cutoff')
    plt.ylabel('Compute Time (log scale)')
    plt.yscale('log')
    plt.title('Effects of Depth Cut-off on Performance')
    plt.legend()
    plt.grid(True, linestyle='dotted')
    plt.show()

# Run experiment
run_experiment()
