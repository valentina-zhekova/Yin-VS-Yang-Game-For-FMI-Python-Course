from board import Board
from player import Player
from random import randint


class Game:

    def __init__(self, user_sign, computer_sign, mode,
                 size, board, start_stones):
        self.user = Player(user_sign)
        self.computer = Player(computer_sign)
        self.board = Board(size, start_stones, board, self.user, self.computer)
        self.mode = mode
        self.does_user_win = None
        self.running = True

    def play_user_turn(self, from_row, from_col, to_row, to_col):
        return self.board.move_stone(self.user, self.computer,
                                     from_row, from_col, to_row, to_col)

    def play_computer_turn(self):
        moves = self.board.possible_moves(self.computer, self.user)
        if moves:
            move = self.__choose_move(moves)
            from_row, from_col = move[0][0], move[0][1]
            to_row, to_col = move[1][0], move[1][1]
            self.board.move_stone(self.computer, self.user,
                                  from_row, from_col, to_row, to_col)
            user_moves = self.board.possible_moves(self.user, self.computer)
            if not user_moves:
                self.end(self.user)
        else:
            self.end(self.computer)

    def __choose_move(self, moves):
        if self.mode == "easy":
            index = randint(0, len(moves) - 1)
            move = moves[index]
        else:
            sorted_by_benefit = sorted(moves, key=lambda tup: tup[2])
            move = sorted_by_benefit[-1]
        return move

    def end(self, player):
        total = self.board.size * self.board.size
        player_points = player.count_of_stones()
        opponent_points = total - player_points
        if player_points != opponent_points:
            self.does_user_win = ((player is self.user and
                                   player_points > opponent_points) or
                                  (player is self.computer and
                                   player_points < opponent_points))
        self.running = False
