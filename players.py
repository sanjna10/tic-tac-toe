from copy import deepcopy
import os
import pickle
import random
from board import Board, PLAYER_ONE, PLAYER_TWO, EMPTY_CELL
import utils

_state_values_for_td_players = {}


class RandomPlayer(object):

    def __init__(self, *, position):
        self.position = position

    @staticmethod
    def play(*, board):
        available_actions = utils.get_available_moves(board)
        return random.choice(available_actions)


class HumanPlayer(object):

    def __init__(self, *, position):
        self.position = position

    @staticmethod
    def play(*, board):
        while True:
            try:
                # Ask the user for the input value
                move = input("Enter your move (e.g. A1): ").strip().upper()
                col = ord(move[0]) - ord('A')
                row = int(move[1:]) - 1
                if board.board[col][row] == EMPTY_CELL:
                    return row, col
                else:
                    print("Cell is already occupied. Try again please.")
            except (IndexError, ValueError):
                print("Invalid input. Please try again.")


class SimpleMinimaxPlayer(object):

    def __init__(self, *, position):
        self.position = position
        self.stats = 0

    def play(self, *, board):
        # Minimax algorithm to choose the optimal move
        best_score = float('-inf')
        best_move = None
        available_moves = utils.get_available_moves(board)

        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax(board, is_maximizing=False)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

    def _minimax(self, board, is_maximizing):
        # Check if the game has ended
        game_ended, there_is_winner = board.game_has_ended()
        self.stats += 1
        if game_ended:
            if there_is_winner:
                return 1 if not is_maximizing else -1
            return 0

        available_moves = utils.get_available_moves(board)

        best_score = float('-inf') if is_maximizing else float('inf')
        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax(board, not is_maximizing)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if is_maximizing:
                best_score = max(score, best_score)
            else:
                best_score = min(score, best_score)
        return best_score


class DynamicProgrammingPlayer(object):

    def __init__(self, *, position):
        self.position = position
        self.state_values = {}
        self.stats = 0

    def play(self, *, board):
        # Use Dynamic Programming to choose the optimal move
        best_score = float('-inf')
        best_move = None
        available_moves = utils.get_available_moves(board)

        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax_cashed(board, is_maximizing=False)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

    def _minimax_cashed(self, board, is_maximizing):
        equiv_board = utils.equivalent_board_representation(board)
        state_key = repr(equiv_board)
        if state_key not in self.state_values:
            self.stats += 1
            # Check if the game has ended
            game_ended, there_is_winner = board.game_has_ended()
            if game_ended:
                if there_is_winner:
                    best_score = 1 if not is_maximizing else -1
                else:
                    best_score = 0
            else:
                available_moves = utils.get_available_moves(board)

                best_score = float('-inf') if is_maximizing else float('inf')
                for row, col in available_moves:
                    board.play_move(row=row, col=col)
                    board.next_player()  # Switch player for minimax algorithm
                    score = self._minimax_cashed(board, not is_maximizing)  # Calculate score using minimax algorithm
                    board.board[col][row] = EMPTY_CELL  # Undo the move
                    board.next_player()  # Switch back to the original player
                    if is_maximizing:
                        best_score = max(score, best_score)
                    else:
                        best_score = min(score, best_score)
            self.state_values[state_key] = best_score
        return self.state_values[state_key]


class MonteCarloPlayer(object):
    def __init__(self, *, position, num_simulations=50):
        self.position = position
        self.num_simulations = num_simulations
        self.stats = 0

    def play(self, *, board):
        # Monte Carlo simulation to choose the best move
        best_move = None
        best_win_rate = float('-inf')
        available_moves = utils.get_available_moves(board)

        for row, col in available_moves:
            wins = 0
            board.play_move(row=row, col=col)
            board.next_player()

            game_ended, there_is_winner = board.game_has_ended()
            if game_ended:
                self.stats += 1
                if there_is_winner:
                    board.board[col][row] = EMPTY_CELL  # Undo the move
                    board.next_player()  # Switch back to original player
                    return row, col
                if best_move is None:
                    best_move = (row, col)
            else:
                # Run simulations to estimate the win rate
                for _ in range(self.num_simulations):
                    wins += self._simulate_game(board)

                win_rate = wins / self.num_simulations
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_move = (row, col)

            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to original player

        return best_move

    def _simulate_game(self, board):
        # Simulate a random game starting with a specific board configuration
        new_board = Board(rows=board.rows, cols=board.cols, connections_to_win=board.connections_to_win,
                          board=deepcopy(board.board), player_to_move=board.current_player)

        opponents_move = True
        while True:
            available_moves = utils.get_available_moves(new_board)
            random_move = random.choice(available_moves)  # Pick a move at random
            new_board.play_move(row=random_move[0], col=random_move[1])
            self.stats += 1
            new_board.next_player()
            game_ended, there_is_winner = new_board.game_has_ended()
            opponents_move = not opponents_move
            if game_ended:
                if there_is_winner:
                    return 1 if opponents_move else -1
                return 0


class TDPlayer(object):

    def __init__(self, *, position, alpha=0.1, gamma=0.9, epsilon=0.1, training_mode=True,
                 state_values_file_name='td_player_values.pkl'):
        self.position = position
        self.alpha = alpha  # Learning rate for Temporal Difference
        self.gamma = gamma  # Discount factor for future rewards
        self.epsilon = epsilon  # Exploration rate
        self.state_values_file = state_values_file_name
        self.training_mode = training_mode
        self.stats = 0

        # Load state values from file, if exists, otherwise initialise as an empty dict
        global _state_values_for_td_players
        if os.path.exists(self.state_values_file) and len(_state_values_for_td_players) == 0:
            with open(self.state_values_file, 'rb') as f:
                _state_values_for_td_players = dict(pickle.load(f))

    @property
    def state_values(self):
        global _state_values_for_td_players
        return _state_values_for_td_players

    def save_new_state_value(self, state_key, new_value):
        global _state_values_for_td_players
        _state_values_for_td_players[state_key] = new_value

        with open(self.state_values_file, 'wb') as f:
            pickle.dump(_state_values_for_td_players, f)

    def play(self, *, board):
        available_moves = utils.get_available_moves(board)

        # See if the game can be terminated in one move
        for row, col in available_moves:
            board.play_move(row=row, col=col)
            game_ended, there_is_winner = board.game_has_ended()
            board.board[col][row] = EMPTY_CELL  # Undo move
            if game_ended:
                self.stats += 1
                # Update the state value with the TD formula:
                # V(s) = V(s) + alpha * ( Reward + gamma * next_value - V(s) )
                # For next_value = 0:
                # V(s) = V(s) + alpha * (Reward - V(s)) = (1-alpha) * V(s) + alpha * Reward
                if there_is_winner:
                    reward = 1 if self.position == PLAYER_ONE else -1
                else:
                    reward = 0
                equiv_board = utils.equivalent_board_representation(board)
                state_key = repr(equiv_board)
                value = self.state_values.get(state_key, 0)
                value = (1 - self.alpha) * value + self.alpha * reward
                self.save_new_state_value(state_key, value)
                return row, col

        # Choose move based on epsilon-greedy strategy
        if self.training_mode and random.random() < self.epsilon:
            # Exploration
            best_move = random.choice(available_moves)
            self.stats += 1
        else:
            # Exploitation
            best_value = float('-inf')
            best_move = None
            for row, col in available_moves:
                self.stats += 1
                board.play_move(row=row, col=col)
                board.next_player()  # Swit ch turn for players
                equiv_board = utils.equivalent_board_representation(board)
                value = (1 if self.position == PLAYER_ONE else -1) * self.state_values.get(repr(equiv_board), 0)
                board.board[col][row] = EMPTY_CELL  # Undo move
                board.next_player()  # Switch turn to original player
                if value > best_value:
                    best_value = value
                    best_move = (row, col)

        # After choosing a move, update the state values using TD formula
        equiv_board = utils.equivalent_board_representation(board)
        state_key = repr(equiv_board)
        value = self.state_values.get(state_key, 0)
        board.play_move(row=best_move[0], col=best_move[1])
        board.next_player()
        equiv_board = utils.equivalent_board_representation(board)
        next_state_key = repr(equiv_board)
        next_value = self.state_values.get(next_state_key, 0)
        board.board[best_move[1]][best_move[0]] = EMPTY_CELL  # Undo move
        board.next_player()

        # Update TD formula
        # V(s) = V(s) + alpha * ( Reward + gamma * next_value - V(s) )
        value = value + self.alpha * (self.gamma * next_value - value)
        self.save_new_state_value(state_key, value)
        return best_move

