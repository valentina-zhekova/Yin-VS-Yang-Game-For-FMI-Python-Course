class Board:

    def __init__(self, dimension, start_stones, player1, player2):
        self.dimension = self.__set_dimension(dimension)
        self.start_stones = self.__set_start_stones(start_stones)
        self.players = self.__set_players()
        self.board = self.__set_board()

    def __set_dimension(self, dimension):
        pass

    def __set_start_stones(self, start_stones):
        pass

    def __set_players(self, player1, player2):
        self.players[player1.stone_type] = player1
        self.players[player2.stone_type] = player2

    def __set_board(self):
        # use dimension, start_stones,
        # self.players, Player.add_stone(), Player.remove_stone()
        pass

    def move_stone(self, player_sign, from_row, from_col, to_row, to_col):
        # use __is_possible_move(), self.players,
        # Player.add_stone(), Player.remove_stone()
        pass

    def __is_possible_move(self, from_row, from_col, to_row, to_col):
        pass

    def possible_moves(self, player_sign):
        # return list of possible moves
        # sorted by decreasing profit for the player
        # use __is_empty_field(), Player.stones
        pass

    def __str__(self):
        pass
