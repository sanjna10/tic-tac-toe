PLAYER_ONE = 1
PLAYER_TWO = 2
EMPTY_CELL = 0
STR_MAPPING = {
    PLAYER_ONE: 'X',
    PLAYER_TWO: 'O',
    EMPTY_CELL: '-',
}


class Board(object):

    def __init__(self, *, rows, cols, connections_to_win, board=None, player_to_move=PLAYER_ONE):
        self.rows = rows
        self.cols = cols
        self.connections_to_win = connections_to_win
        self.current_player = player_to_move
        self.board = [[EMPTY_CELL] * self.rows for _ in range(self.cols)] if board is None else board

    @staticmethod
    def _cell_to_str(cell):
        return STR_MAPPING[cell]

    def __str__(self):
        res_str = '\n'.join(
            f'  {row + 1} | ' + ' '.join(self._cell_to_str(self.board[col][row]) for col in range(self.cols))
            for row in range(self.rows)
        )
        res_str += '\n' + 5 * '-' + 2*self.cols*'-' + '\n'
        letters = [chr(i) for i in range(ord('A'), ord('A') + self.cols)]
        res_str += 6 * ' ' + ' '.join(letters) + '\n'
        return res_str

    def __repr__(self):
        board_repr = f"{self.current_player}"
        for col in range(self.cols):
            board_repr += '|' + ''.join([str(plr_type) for plr_type in self.board[col]])
        return board_repr

    def next_player(self):
        self.current_player = PLAYER_ONE if self.current_player == PLAYER_TWO else PLAYER_TWO

    def play_move(self, *, row, col):
        assert self.board[col][row] == EMPTY_CELL, f"The cell {row, col} is not empty."
        self.board[col][row] = self.current_player

    def game_has_ended(self):
        if (self._horizontal_check() or self._vertical_check() or self._diagonal_increasing_check() or
                self._diagonal_decreasing_check()):
            return True, True
        elif all([self.board[col][row] != EMPTY_CELL for col in range(self.cols) for row in range(self.rows)]):
            return True, False
        return False, False

    def _horizontal_check(self):
        for row in range(self.rows):
            for col in range(self.cols - self.connections_to_win + 1):
                if (all([self.board[col + i][row] == self.board[col][row] for i in range(self.connections_to_win)])
                        and self.board[col][row] != EMPTY_CELL):
                    return True
        return False

    def _vertical_check(self):
        for col in range(self.cols):
            for row in range(self.rows - self.connections_to_win + 1):
                if (all([self.board[col][row+i] == self.board[col][row] for i in range(self.connections_to_win)])
                        and self.board[col][row] != EMPTY_CELL):
                    return True
        return False

    def _diagonal_increasing_check(self):
        for col in range(self.cols - self.connections_to_win +1):
            for row in range(self.rows - self.connections_to_win + 1):
                if (all(self.board[col+i][row+i] == self.board[col][row] for i in range(self.connections_to_win))
                        and self.board[col][row] != EMPTY_CELL):
                    return True
        return False

    def _diagonal_decreasing_check(self):
        for col in range(self.cols - self.connections_to_win + 1):
            for row in range(self.rows - self.connections_to_win + 1):
                start_row = row + self.connections_to_win - 1
                if (all(self.board[col + i][start_row - i] == self.board[col][start_row] for i in range(self.connections_to_win))
                        and self.board[col][start_row] != EMPTY_CELL):
                    return True
        return False


if __name__ == '__main__':
    board = Board(rows=3, cols=4, connections_to_win=3)
    board.play_move(row=2, col=0)
    board.play_move(row=1, col=1)
    board.play_move(row=0, col=2)
    print(board)
    print(repr(board))
    print(board._horizontal_check())
    print(board._vertical_check())
    print(board._diagonal_decreasing_check())
    print(board._diagonal_increasing_check())
