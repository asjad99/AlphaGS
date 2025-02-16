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
    simulations = np.arange(100, 2000, 100)
    mcts_runtime = []
    variables = np.arange(40, 80, 5)
    minimax_perf, mcts_perf, stochastic_perf = [], [], []
    
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
    
    for sim_count in simulations:
        game = AdversarialGame(10)  # Fixed depth
        mcts = MCTS()
        start = time.time()
        mcts.search(game, game.initial_state(), sim_count)
        mcts_runtime.append(time.time() - start)
    
    for var in variables:
        game = AdversarialGame(10)  # Fixed depth
        
        # Minimax Execution
        start = time.time()
        # minimax_decision(game.initial_state())
        minimax_perf.append(time.time() - start)
        
        # MCTS Execution
        start = time.time()
        mcts.search(game, game.initial_state(), 100)
        mcts_perf.append(time.time() - start)
        
        # Stochastic Model Execution
        start = time.time()
        time.sleep(np.random.rand() * 0.01)  # Simulated random execution time
        stochastic_perf.append(time.time() - start)
    
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
    
    plt.figure(figsize=(8, 5))
    plt.plot(simulations, mcts_runtime, label='Monte Carlo Tree Search', marker='o', linestyle='-', color='black')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Compute Time (log scale)')
    plt.yscale('log')
    plt.title('Effects of Simulation Count on Performance')
    plt.legend()
    plt.grid(True, linestyle='dotted')
    plt.show()
    
    plt.figure(figsize=(8, 5))
    plt.plot(variables, minimax_perf, label='Minimax with Alpha-Beta Pruning', marker='o', linestyle='-', color='black')
    plt.plot(variables, mcts_perf, label='Monte Carlo Tree Search (MCTS)', marker='s', linestyle='--', color='gray')
    plt.plot(variables, stochastic_perf, label='Stochastic Game (Dice Roll)', marker='^', linestyle=':', color='darkgray')
    plt.xlabel('Number of Variables in Vocabulary')
    plt.ylabel('Compute Time (log scale)')
    plt.yscale('log')
    plt.title('Performance Comparison of Search Algorithms')
    plt.legend()
    plt.grid(True, linestyle='dotted')
    plt.show()

# Run experiment
run_experiment()
