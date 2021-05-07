## A Framework for decision making in adversarial settings to acheive strategic resilience 


### About the Project: 
This paper studies the problem of strategic resilience, and provides the principled computational underpinnings of the reasoning that businesses should engage in to make critical strategic choices. We propose an approach to semi-automatically assist businesses with strategic decision making, the argument being that such decision making can be made more resilient by basing the analysis on organizational goal models in combination with game tree search.  We asssume  the presence of adversarial forces in decision making and we cast decision making problem as game playing (using game tree search) which is an interesting and a novel take on decision support. 

(i) The proposed framework considers both strategic resilience (the ability to recover quickly from difficulties) and robustness (the ability to withstand or overcome adverse conditions).
(ii) The experimental evaluation verifies the effectiveness of the algorithms in which we show automatic decision support based on goal hierarchies that have OR refinement relations by using MINIMAX and Monte Carlo Tree Search.

A prototype is made where two different types of search are implemented (MINIMAX search and Monte Carlo Tree Search), and execution times for the search are analysed. The paper looks at the utilisation of mainly two algorithms, Min-Max and Monte Carlo for optimising choices in a tree. The tree corresponds to goal model and it is argued that this imitate how businesses think when making competitor analysis and the corresponding planning.

read the blog post for more details: https://www.asjadk.io/strategic_resilience/ 


### Project Structure

This Project is a prototype with following structure: 

  - SAT Solver(found in logic.py) to perform  game tree search to arrive at the decision.
  - Monte-Carlo Search(mcts.py). Both Librbaries are included and can be replaced with other state of the Art implementations. 
  - action_effect_table.py and condition_action_rules.py - We encode the current state of business and the environment its operating in using assertions in the form of of truth-functional assertions and condition-actions rules representing the current capabilities(of the business).
  - 
### Usage
```
Python main.py
```
