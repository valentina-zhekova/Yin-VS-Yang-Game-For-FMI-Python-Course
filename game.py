from board import Board
from player import Player


class Game:

    def __init__(self, user_stone_type, computer_stone_type, mode,
                 board=None, dimension=None, start_stones=None):
        self.user = self.__set_player(user_stone_type)
        self.computer = self.__set_player(computer_stone_type)
        self.board = self.__set_board(board, dimension, start_stones,
                                      self.user, self.computer)
        self.mode = self.__set_mode(mode)
        self.does_user_win = None

    def __set_board(board, dimension, start_stones, player1, player2):
        # if not unfinished game make new board
        pass

    def __set_player(self, user_stone_type):
        pass

    def __set_mode(self, mode):
        pass

    def play_user_turn(self, row, col):
        # call board.possible_moves()
        # if hasn't more moves call end(), otherwise:
        # call board.move_stone()
        # call play_computer_turn()
        # return if the operation was succesful
        pass

    def play_computer_turn(self):
        # call board.possible_moves()
        # if hasn't more moves call end(), otherwise:
        # choose a move according to self.mode
        # call board.move_stone()
        pass

    def end(self):
        # calculate result
        # set self.does_user_win
        pass
