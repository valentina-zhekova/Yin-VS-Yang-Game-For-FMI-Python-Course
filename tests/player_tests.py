import sys
import unittest

sys.path.append("..")
from player import Player


class PlayerTests(unittest.TestCase):

    def setUp(self):
        self.player = Player("O")

    def test_player_sign(self):
        self.assertEqual("O", self.player.sign)

    def test_add_stone(self):
        self.assertEqual([], self.player.stones)
        self.player.add_stone(1, 1)
        self.assertEqual([(1, 1)], self.player.stones)

    def test_add_stone_already_owned(self):
        self.player.add_stone(1, 1)
        self.player.add_stone(1, 1)
        self.assertEqual([(1, 1)], self.player.stones)

    def test_remove_stone(self):
        self.player.add_stone(1, 1)
        self.player.remove_stone(1, 1)
        self.assertEqual([], self.player.stones)

    def test_remove_stone_not_owned(self):
        self.player.remove_stone(1, 1)
        self.assertEqual([], self.player.stones)

    def test_count_of_stones(self):
        self.assertEqual(0, self.player.count_of_stones())
        self.player.add_stone(1, 1)
        self.player.add_stone(4, 2)
        self.assertEqual(2, self.player.count_of_stones())


if __name__ == '__main__':
    unittest.main()
