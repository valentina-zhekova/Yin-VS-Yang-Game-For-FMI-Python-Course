import sys
import unittest

sys.path.append("..")
from board import Board
from player import Player


class BoardTests(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("X")
        self.player2 = Player("O")
        self.board = Board(4, 4, None, self.player1, self.player2)

    def test_are_fields_assigned(self):
        self.assertEqual(4, self.board.size)
        self.assertEqual(4, self.board._Board__start_stones)
        self.assertEqual((self.player1, self.player2),
                         self.board._Board__players)
        self.assertEqual([['X', 'X', 'X', 'X'],
                          ['_', '_', '_', '_'],
                          ['_', '_', '_', '_'],
                          ['O', 'O', 'O', 'O']], self.board._Board__board)

    def test__set_board_for_loaded_board(self):
        loaded_board = ["X,O", "O,X"]
        self.assertEqual([['X', 'O'],
                          ['O', 'X']],
                         self.board._Board__set_board(loaded_board))

    def test__set_board_by_parameteres(self):
        self.board.size = 6
        self.board._Board__start_stones = 1
        self.assertEqual([['X', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', '_'],
                          ['_', '_', '_', '_', '_', 'O']],
                         self.board._Board__set_board(None))

    def test__load_board(self):
        board = ["X,X", "O,O"]
        self.assertEqual([['X', 'X'],
                          ['O', 'O']],
                         self.board._Board__load_board(board))

    def test__set_board_row(self):
        self.board.size = 3
        self.assertEqual(['*', '*', '*'],
                         self.board._Board__set_board_row('*', 7))

    def test_move_stone_jump_step(self):
        self.assertTrue(
            self.board.move_stone(self.player2, self.player1, 3, 0, 1, 1))
        self.assertEqual([['O', 'O', 'O', 'X'],
                          ['_', 'O', '_', '_'],
                          ['_', '_', '_', '_'],
                          ['_', 'O', 'O', 'O']], self.board._Board__board)

    def test_move_stone_clone_step(self):
        self.assertTrue(
            self.board.move_stone(self.player2, self.player1, 3, 1, 2, 0))
        self.assertEqual([['X', 'X', 'X', 'X'],
                          ['_', '_', '_', '_'],
                          ['O', '_', '_', '_'],
                          ['O', 'O', 'O', 'O']], self.board._Board__board)

    def test_move_stone_not_a_player_stone_at_from_field(self):
        self.assertFalse(
            self.board.move_stone(self.player2, self.player1, 2, 1, 1, 1))

    def test_move_stone_not_a_free_to_field(self):
        self.assertFalse(
            self.board.move_stone(self.player2, self.player1, 3, 1, 3, 2))

    def test_move_stone_out_of_range(self):
        self.assertFalse(
            self.board.move_stone(self.player2, self.player1, 3, 3, 2, 4))
        self.assertFalse(
            self.board.move_stone(self.player2, self.player1, 3, 4, 2, 1))
        self.assertFalse(
            self.board.move_stone(self.player2, self.player1, 3, 0, 1, 3))

    def test__is_possible_move_clone_step(self):
        self.board.size = 5
        self.board._Board__board = [['_', '_', '_', '_', '_'],
                                    ['_', '_', '_', '_', '_'],
                                    ['_', '_', 'X', '_', '_'],
                                    ['_', '_', '_', '_', '_'],
                                    ['_', '_', '_', '_', '_']]
        self.assertTrue(self.board._Board__is_possible_move(2, 2, 1, 1))
        self.assertTrue(self.board._Board__is_possible_move(2, 2, 3, 3))

    def test__is_possible_move_jump_step(self):
        self.board.size = 5
        self.board._Board__board = [['_', '_', '_', '_', '_'],
                                    ['_', '_', '_', '_', '_'],
                                    ['_', '_', 'X', '_', '_'],
                                    ['_', '_', '_', '_', '_'],
                                    ['_', '_', '_', '_', '_']]
        self.assertTrue(self.board._Board__is_possible_move(2, 2, 0, 0))
        self.assertTrue(self.board._Board__is_possible_move(2, 2, 4, 4))

    def test__is_possible_move_from_field_to_same_field(self):
        self.assertFalse(self.board._Board__is_possible_move(3, 1, 3, 1))

    def test__is_possible_move_out_of_board_bounds(self):
        self.assertFalse(self.board._Board__is_possible_move(3, 3, 2, 4))
        self.assertFalse(self.board._Board__is_possible_move(3, 4, 2, 1))

    def test__is_possible_move_out_of_field_range(self):
        self.assertFalse(self.board._Board__is_possible_move(3, 0, 1, 3))

    def test__is_in_board_range(self):
        self.assertFalse(self.board._Board__is_in_board_range(7))
        self.assertTrue(self.board._Board__is_in_board_range(3))

    def test__is_in_field_range(self):
        self.assertFalse(self.board._Board__is_in_field_range(2, 5))
        self.assertTrue(self.board._Board__is_in_field_range(2, 0))

    def test__convert_opponent_stones(self):
        self.board._Board__board = [['O', 'X', 'X'],
                                    ['O', '_', 'X'],
                                    ['O', 'O', 'X']]
        self.board._Board__convert_opponent_stones(
            1, 1, self.player1, self.player2)
        self.assertTrue([['X', 'X', 'X'],
                         ['X', '_', 'X'],
                         ['X', 'X', 'X']], self.board._Board__board)

    def test__opponent_stones(self):
        self.board._Board__board = [['O', 'X', 'X'],
                                    ['O', '_', 'X'],
                                    ['O', 'O', 'X']]
        self.assertEqual([(0, 0), (1, 0), (2, 0), (2, 1)],
                         self.board._Board__opponent_stones(
                            1, 1, self.player2))

    def test__is_not_neighbour_move(self):
        self.board.size = 5
        self.board._Board__board = [['_', '_', '_', '_', '_'],
                                    ['_', '_', '_', '_', '_'],
                                    ['_', '_', 'X', '_', '_'],
                                    ['_', '_', '_', '_', '_'],
                                    ['_', '_', '_', '_', '_']]
        self.assertFalse(self.board._Board__is_not_neighbour_move(2, 2, 2, 3))
        self.assertTrue(self.board._Board__is_not_neighbour_move(2, 2, 0, 4))
        self.assertTrue(self.board._Board__is_not_neighbour_move(2, 2, 4, 0))

    def test_possible_moves(self):
        possibilities = [((0, 0), (1, 0), 1), ((0, 0), (1, 1), 1),
                         ((0, 0), (1, 2), 0), ((0, 0), (2, 0), 2),
                         ((0, 0), (2, 1), 3), ((0, 0), (2, 2), 3)]
        self.assertEqual(possibilities, self.board.possible_moves(
                            self.player1, self.player2)[:6])

    def test__str__method(self):
        output = ("    0  1  2  3  \n\n" +
                  "0   X  X  X  X \n" +
                  "1   _  _  _  _ \n" +
                  "2   _  _  _  _ \n" +
                  "3   O  O  O  O \n")
        self.assertEqual(output, str(self.board))

    def test_database_format(self):
        self.assertEqual("X|X,X,X,X|_,_,_,_|_,_,_,_|O,O,O,O",
                         self.board.database_format())

if __name__ == '__main__':
    unittest.main()
