from tqdm import tqdm
from board import Board, PLAYER_ONE, PLAYER_TWO
from players import HumanPlayer, RandomPlayer, SimpleMinimaxPlayer, DynamicProgrammingPlayer, MonteCarloPlayer, TDPlayer

_player_categories = {
    'human_user': HumanPlayer,
    'random_player': RandomPlayer,
    'minimax_player': SimpleMinimaxPlayer,
    'dp_player': DynamicProgrammingPlayer,
    'mc_player': MonteCarloPlayer,
    'td_player': TDPlayer,
}
wins_p1 = 0
wins_p2 = 0
draws = 0


class TicTacToe(object):

    def __init__(self, *, player_one, player_two, display_board=True):
        self.board = Board(rows=3, cols=3, connections_to_win=3)
        self.display_board = display_board
        self.current_player = _player_categories[player_one](position=PLAYER_ONE)
        self.next_player = _player_categories[player_two](position=PLAYER_TWO)

    def play_game(self):
        while True:
            if self.display_board:
                print(self.board)
                print(f"Player {'X' if self.current_player.position == PLAYER_ONE else 'O'}'s turn\n\n")
            row, col = self.current_player.play(board=self.board)
            self.board.play_move(row=row, col=col)
            game_ended, there_is_winner = self.board.game_has_ended()
            if game_ended:
                global wins_p1, wins_p2, draws
                if there_is_winner and self.current_player.position == PLAYER_ONE:
                    wins_p1 += 1
                elif there_is_winner and self.current_player.position == PLAYER_TWO:
                    wins_p2 += 1
                else:
                    draws += 1

                # if self.current_player.position == PLAYER_ONE:
                # #     print(f"Stats Player 1: {self.current_player.stats}")
                # #     print(f"Stats Player 2: {self.next_player.stats}")
                # # else:
                # #     print(f"Stats Player 1: {self.next_player.stats}")
                # #     print(f"Stats Player 2: {self.current_player.stats}")
                if self.display_board:
                    print(self.board)
                    if there_is_winner:
                        print(f"Player {'X' if self.current_player.position == PLAYER_ONE else 'O'} wins!")
                    else:
                        print("It's a draw!")
                break
            self.current_player, self.next_player = self.next_player, self.current_player
            self.board.next_player()


if __name__ == '__main__':
    # for _ in tqdm(range(3000), "Simulations: "):
    #     game = TicTacToe(player_one='td_player', player_two='td_player', display_board=False)
    #     game.play_game()

    for _ in tqdm(range(50), "Number of games: "):
        # game = TicTacToe(player_one='dp_player', player_two='minimax_player', display_board=False)
        # game = TicTacToe(player_one='mc_player', player_two='dp_player', display_board=False)
        # game = TicTacToe(player_one='td_player', player_two='dp_player', display_board=False)
        game = TicTacToe(player_one='dp_player', player_two='td_player', display_board=False)
        game.play_game()

    print(f"Wins for Player 1: {wins_p1}")
    print(f"Wins for Player 2: {wins_p2}")
    print(f"Draws: {draws}")
