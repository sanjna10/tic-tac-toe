# Intelligent Tic-Tac-Toe: Search and Reinforcement Learning Agents

A Python-based Tic-Tac-Toe project that combines classic game search with reinforcement learning. The project supports multiple player strategies, including human interaction, random play, Minimax search, Dynamic Programming, Monte Carlo methods, and Temporal Difference (TD) learning.

## Project Highlights

- Implemented multiple Tic-Tac-Toe agents with different decision-making strategies
- Supports both interactive gameplay and automated AI-vs-AI simulations
- Includes search-based methods such as **Minimax** and **Dynamic Programming**
- Includes learning-based agents such as **Monte Carlo** and **Temporal Difference (TD) Learning**
- Saves learned state values for the TD player using a persistent `.pkl` file

## Features

- Human vs Human gameplay
- Human vs AI gameplay
- AI vs AI simulations
- Reusable board-state utilities
- Persistent TD learning across runs
- Easy-to-modify player configurations

```markdown
## How to Run the Project

Make sure all project files (`board.py`, `players.py`, `tictactoe.py`, `utils.py`, and optionally `td_player_values.pkl`) are in the same folder. Then open a terminal in that folder and run:

```bash
python tictactoe.py