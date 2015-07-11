import sys
import unittest

sys.path.append("..")
from game import Game


class GameTests(unittest.TestCase):

    def setUp(self):
        self.game = Game('X', 'O', "easy", 4, None, 4)

    def test_are_fields_assigned(self):
        self.assertEqual('X', self.game.user.sign)
        self.assertEqual('O', self.game.computer.sign)
        self.assertEqual([['X', 'X', 'X', 'X'],
                          ['_', '_', '_', '_'],
                          ['_', '_', '_', '_'],
                          ['O', 'O', 'O', 'O']],
                         self.game.board._Board__board)
        self.assertEqual("easy", self.game.mode)
        self.assertEqual(None, self.game.does_user_win)
        self.assertEqual(True, self.game.running)

    def test_play_user_turn(self):
        self.assertTrue(self.game.play_user_turn(0, 3, 2, 4))
        self.assertEqual([['X', 'X', '_', 'X'],
                          ['_', '_', '_', '_'],
                          ['_', '_', '_', 'X'],
                          ['O', 'O', 'X', 'X']],
                         self.game.board._Board__board)

    def test_play_user_turn_impossible(self):
        self.assertFalse(self.game.play_user_turn(0, 4, 2, 1))
        self.assertEqual([['X', 'X', 'X', 'X'],
                          ['_', '_', '_', '_'],
                          ['_', '_', '_', '_'],
                          ['O', 'O', 'O', 'O']],
                         self.game.board._Board__board)

    def test_play_computer_turn(self):
        self.game.play_computer_turn()
        self.assertTrue(self.game.running)
        self.assertNotEqual([['X', 'X', 'X', 'X'],
                             ['_', '_', '_', '_'],
                             ['_', '_', '_', '_'],
                             ['O', 'O', 'O', 'O']],
                            self.game.board._Board__board)

    def test_play_computer_turn_no_more_moves_for_computer(self):
        self.game.board._Board__board = [['X', 'X', 'X', 'X'],
                                         ['X', 'X', 'X', 'X'],
                                         ['X', 'X', 'X', 'X'],
                                         ['O', 'O', 'O', 'O']]
        self.game.play_computer_turn()
        self.assertFalse(self.game.running)

    def test_play_computer_turn_no_more_user_moves(self):
        self.game.board._Board__board = [['X', 'X', 'X', 'X'],
                                         ['X', 'X', '_', 'X'],
                                         ['X', 'X', 'X', 'X'],
                                         ['O', 'O', 'O', 'O']]
        self.game.play_computer_turn()
        self.assertFalse(self.game.running)

    def test__choose_move_hard_mode(self):
        self.game.board._Board__board = [['X', 'X', 'X', 'X'],
                                         ['X', '_', '_', 'O']
                                         ['_', 'O', '_', 'O'],
                                         ['O', 'O', 'O', 'O']]
        possible_moves = [((3, 0), (1, 1), 4), ((3, 0), (2, 0), 1),
                          ((3, 0), (1, 2), 3), ((3, 0), (2, 2), 0),
                          ((3, 1), (1, 1), 4), ((3, 1), (2, 0), 1),
                          ((3, 1), (1, 2), 3), ((3, 1), (2, 2), 1),
                          ((3, 2), (1, 1), 4), ((3, 2), (2, 0), 0),
                          ((3, 2), (1, 2), 3), ((3, 2), (2, 2), 1),
                          ((3, 3), (1, 1), 4), ((3, 3), (1, 2), 3),
                          ((3, 3), (2, 2), 1), ((2, 3), (1, 1), 4),
                          ((2, 3), (1, 2), 4), ((2, 3), (2, 2), 1),
                          ((1, 3), (1, 1), 4), ((1, 3), (1, 2), 4),
                          ((1, 3), (2, 2), 1), ((2, 1), (1, 1), 5),
                          ((2, 1), (2, 0), 2), ((2, 1), (1, 2), 4),
                          ((2, 1), (2, 2), 1)]
        self.assertEqual(((2, 1), (1, 1), 5),
                         self.game._Game__chose_move(possible_moves))

    def test_end_user_wins(self):
        self.game.board._Board__board = [['X', 'X', 'X', 'X'],
                                         ['X', 'X', 'X', 'X'],
                                         ['X', 'X', 'X', 'X'],
                                         ['O', 'O', 'O', 'O']]
        self.end(self.game.user)
        self.assertTrue(self.game.does_user_win)
        self.assertFalse(self.game.running)

    def test_end_computer_wins(self):
        self.game.board._Board__board = [['X', 'X', 'X', 'X'],
                                         ['O', 'O', 'O', 'O'],
                                         ['O', 'O', 'O', 'O'],
                                         ['O', 'O', 'O', 'O']]
        self.end(self.game.user)
        self.assertFalse(self.game.does_user_win)
        self.assertNotEqual(None, self.game.does_user_win)
        self.assertFalse(self.game.running)

    def test_end_equal(self):
        self.game.board._Board__board = [['X', 'X', 'X', 'X'],
                                         ['X', 'X', 'X', 'X'],
                                         ['O', 'O', 'O', 'O'],
                                         ['O', 'O', 'O', 'O']]
        self.end(self.game.user)
        self.assertFalse(self.game.does_user_win)
        self.assertEqual(None, self.game.does_user_win)
        self.assertFalse(self.game.running)

if __name__ == '__main__':
    unittest.main()
