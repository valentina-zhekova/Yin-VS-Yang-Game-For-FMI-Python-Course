class Board:

    EMPTY_SIGN = '_'

    def __init__(self, feasible_size, feasible_start_stones,
                 board, player1, player2):
        self.size = feasible_size
        self.__start_stones = feasible_start_stones
        self.__players = (player1, player2)
        self.__board = self.__set_board(board)

    def __set_board(self, board):
        if board:
            result = self.__load_board(board)
        else:
            if self.__start_stones == 1:
                result = self.__set_board_one_stone()
            else:
                result = self.__set_board_stones_divisible_by_size()
        return result

    def __load_board(self, board):
        return [row.split(",") for row in board]

    def __set_board_one_stone(self):
        result = [self.__set_row() for row in range(self.size)]
        for index, player_index in [(0, 0), (self.size - 1, 1)]:
            result[index][index] = self.__players[player_index].sign
            self.__players[player_index].add_stone(index, index)
        return result

    def __set_board_stones_divisible_by_size(self):
        result = []
        k = self.__start_stones // self.size
        n = self.size
        for row in range(k):
            result.append(self.__set_row(self.__players[0], row))
        for row in range(k, n - k):
            result.append(self.__set_row())
        for row in range(n - k, n):
            result.append(self.__set_row(self.__players[1], row))
        return result

    def __set_row(self, player=None, row_index=None, sign=EMPTY_SIGN,):
        row = []
        for col in range(self.size):
            if player:
                player.add_stone(row_index, col)
                sign = player.sign
            row.append(sign)
        return row

    def move_stone(self, player, opponent, from_row, from_col, to_row, to_col):
        is_successful = False
        in_range = self.__is_possible_move(from_row, from_col, to_row, to_col)
        if in_range:
            accurate_pick = (self.__board[from_row][from_col] == player.sign)
            if accurate_pick:
                self.__convert_stones(to_row, to_col, player, opponent)
                if self.__is_jump_step(from_row, from_col, to_row, to_col):
                    player.remove_stone(from_row, from_col)
                    self.__board[from_row][from_col] = Board.EMPTY_SIGN
                player.add_stone(to_row, to_col)
                self.__board[to_row][to_col] = player.sign
                is_successful = True
        return is_successful

    def __is_possible_move(self, from_row, from_col, to_row, to_col):
        is_in_bounds = (self.__is_in_board_range(to_row) and
                        self.__is_in_board_range(to_col) and
                        self.__is_in_board_range(from_row) and
                        self.__is_in_board_range(from_col))
        if is_in_bounds:
            is_empty = (self.__board[to_row][to_col] == Board.EMPTY_SIGN)
            is_different = (from_row != to_row) or (from_col != to_col)
            is_in_range = (self.__is_in_field_range(from_row, to_row) and
                           self.__is_in_field_range(from_col, to_col))
        return (is_in_bounds and is_empty and is_different and is_in_range)

    def __is_in_board_range(self, index):
        return (0 <= index) and (index < self.size)

    def __is_in_field_range(self, from_index, to_index):
        return (from_index - 2) <= to_index and to_index <= (from_index + 2)

    def __convert_stones(self, by_row, by_col, player, opponent):
        for stone in self.__opponent_stones(by_row, by_col, opponent):
            row, col = stone[0], stone[1]
            opponent.remove_stone(row, col)
            player.add_stone(row, col)
            self.__board[row][col] = player.sign

    def __opponent_stones(self, by_row, by_col, opponent):
        result = []
        for row in range(by_row - 1, by_row + 2):
            for col in range(by_col - 1, by_col + 2):
                is_in_bounds = (self.__is_in_board_range(row) and
                                self.__is_in_board_range(col))
                if is_in_bounds:
                    opponent_stone = (self.__board[row][col] == opponent.sign)
                    if opponent_stone:
                        result.append((row, col))
        return result

    def __is_jump_step(self, from_row, from_col, to_row, to_col):
        return (((to_row < from_row - 1) or (from_row + 1 < to_row)) or
                ((to_col < from_col - 1) or (from_col + 1 < to_col)))

    def possible_moves(self, player, opponent):
        result = []
        for stone in player.stones:
            by_row, by_col = stone[0], stone[1]
            for row in range(by_row - 2, by_row + 3):
                for col in range(by_col - 2, by_col + 3):
                    if self.__is_possible_move(by_row, by_col, row, col):
                        to_convert = self.__opponent_stones(row, col, opponent)
                        benefit = len(to_convert)
                        if not self.__is_jump_step(by_row, by_col, row, col):
                            benefit += 1
                        result.append((stone, (row, col), benefit))
        return result

    def __str__(self):
        result = ""
        horizontal_index_line = "    "
        for col in range(self.size):
            horizontal_index_line += str(col) + " "
            if col < 10:
                horizontal_index_line += " "
        result += horizontal_index_line + "\n\n"
        for row in range(self.size):
            vertical_index = str(row) + " "
            if row < 10:
                vertical_index += " "
            vertical_index += " "
            result += vertical_index + "  ".join(self.__board[row]) + " \n"
        return result

    def database_format(self):
        rows = [",".join(row) for row in self.__board]
        return self.__players[0].sign + '|' + "|".join(rows)
