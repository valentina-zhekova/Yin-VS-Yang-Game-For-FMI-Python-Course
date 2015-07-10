class Player:

    def __init__(self, sign):
        self.stones = []
        self.sign = sign

    def add_stone(self, row, col):
        stone = (row, col)
        if stone not in self.stones:
            self.stones.append(stone)

    def remove_stone(self, row, col):
        stone = (row, col)
        if stone in self.stones:
            self.stones.remove(stone)

    def count_of_stones(self):
        return len(self.stones)
