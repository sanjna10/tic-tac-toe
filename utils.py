import numpy as np
from board import Board, EMPTY_CELL


def get_available_moves(board):
    available_moves = []
    for col in range(board.cols):
        for row in range(board.rows):
            if board.board[col][row] == EMPTY_CELL:
                available_moves.append((row, col))
    return available_moves


def equivalent_board_representation(board):
    # Convert the board to a numpy array for easy manipulation
    board_array = np.array(board.board)
    equivalent_positions = set([])

    for _ in range(4):
        board_tuple = tuple(map(tuple, board_array))
        equivalent_positions.add(board_tuple)
        board_array = np.rot90(board_array, k=1)

    reflected_board = np.transpose(board_array)
    for _ in range(4):
        board_tuple = tuple(map(tuple, reflected_board))
        equivalent_positions.add(board_tuple)
        reflected_board = np.rot90(reflected_board, k=1)

    representative_position = max(equivalent_positions)
    representative_board = Board(rows=board.rows,
                                 cols=board.cols,
                                 connections_to_win=board.connections_to_win,
                                 player_to_move=board.current_player,
                                 board=[list(tup) for tup in representative_position]
                                 )
    return representative_board


if __name__ == '__main__':
    _board = Board(rows=3, cols=3, connections_to_win=3)
    _board.play_move(row=0, col=2)
    _board.next_player()
    _board.play_move(row=0, col=1)
    _board.next_player()
    print(_board)

    _repr_board = equivalent_board_representation(_board)
    print(_repr_board)
