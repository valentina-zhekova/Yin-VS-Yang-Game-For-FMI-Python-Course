class Board:

    def __init__(self, feasible_size, feasible_start_stones,
                 board, player1, player2):
        self.__size = feasible_size
        self.__start_stones = feasible_start_stones
        self.__players = (player1, player2)
        self.__board = self.__set_board(board)

    def __set_board(self, board):
        if board:
            result = self.__load_board(board)
        else:
            result = []
            if self.__start_stones == 1:
                for index in range(self.__size):
                    row = []
                    for col in range(self.__size):
                        row.append('_')
                    result.append(row)
                result[0][0] = self.__players[0].sign
                self.__players[0].add_stone(0, 0)
                n = self.__size - 1
                result[n][n] = self.__players[1].sign
                self.__players[1].add_stone(n, n)
            else:
                k = self.__start_stones // self.__size
                n = self.__size
                for row in range(k):
                    result.append(self.__set_board_row(self.__players[0].sign,
                                                       row, self.__players[0]))
                for row in range(k, n - k):
                    result.append(self.__set_board_row('_', row))
                for row in range(n - k, n):
                    result.append(self.__set_board_row(self.__players[1].sign,
                                                       row, self.__players[1]))
        return result

    def __load_board(self, board):
        result = []
        for row in board:
            result.append(row.split(","))
        return result

    def __set_board_row(self, sign, row_index, player=None):
        row = []
        for col in range(self.__size):
            row.append(sign)
            if player:
                player.add_stone(row_index, col)
        return row

    def move_stone(self, player, opponent,
                   from_row, from_col, to_row, to_col):
        in_range = self.__is_possible_move(from_row, from_col, to_row, to_col)
        if in_range:
            accurate_pick = self.__board[from_row][from_col] == player.sign
            if accurate_pick:
                self.__convert_opponent_stones(to_row, to_col,
                                               player, opponent)
                if self.__is_not_neighbour_move(from_row, from_col,
                                                to_row, to_col):
                    player.remove_stone(from_row, from_col)
                    self.__board[from_row][from_col] = '_'
                player.add_stone(to_row, to_col)
                self.__board[to_row][to_col] = player.sign
                return True
            else:
                return False
        else:
            return False

    def __is_possible_move(self, from_row, from_col, to_row, to_col):
        is_in_board_bounds = (self.__is_in_board_range(to_row) and
                              self.__is_in_board_range(to_col) and
                              self.__is_in_board_range(from_row) and
                              self.__is_in_board_range(from_col))
        if is_in_board_bounds:
            is_field_empty = self.__board[to_row][to_col] == '_'
        is_different_field = (from_row != to_row) or (from_col != to_col)
        is_in_far_range = (self.__is_in_field_range(from_row, to_row) and
                           self.__is_in_field_range(from_col, to_col))
        return (is_in_board_bounds and is_field_empty and
                is_different_field and is_in_far_range)

    def __is_in_board_range(self, index):
        return 0 <= index and index < self.__size

    def __is_in_field_range(self, from_index, to_index):
        return (from_index - 2) <= to_index and to_index <= (from_index + 2)

    def __convert_opponent_stones(self, by_row, by_col,
                                  player, opponent):
        for stone in self.__opponent_stones(by_row, by_col, opponent):
            row, col = stone[0], stone[1]
            opponent.remove_stone(row, col)
            player.add_stone(row, col)
            self.__board[row][col] = player.sign

    def __opponent_stones(self, by_row, by_col, opponent):
        result = []
        for row in range(by_row - 1, by_row + 2):
            for col in range(by_col - 1, by_col + 2):
                is_in_board_bounds = (self.__is_in_board_range(row) and
                                      self.__is_in_board_range(col))
                if is_in_board_bounds:
                    is_opponent_stone = self.__board[row][col] == opponent.sign
                    if is_opponent_stone:
                        result.append((row, col))
        return result

    def __is_not_neighbour_move(self, from_row, from_col, to_row, to_col):
        return (((to_row < from_row - 1) or (from_row + 1 < to_row)) or
                ((to_col < from_col - 1) or (from_col + 1 < to_col)))

    def possible_moves(self, player, opponent):
        result = []
        for stone in player.stones:
            row = stone[0]
            col = stone[1]
            for r in range(row - 2, row + 3):
                for c in range(col - 2, col + 3):
                    if self.__is_possible_move(row, col, r, c):
                        benefit = len(self.__opponent_stones(r, c, opponent))
                        if not self.__is_not_neighbour_move(row, col, r, c):
                            benefit += 1
                        result.append((stone, (r, c), benefit))
        return result

    def __str__(self):
        result = ""

        horizontal_index_line = "    "
        for col in range(self.__size):
            horizontal_index_line += str(col) + " "
            if col < 10:
                horizontal_index_line += " "
        result += horizontal_index_line + "\n\n"

        for row in range(self.__size):
            vertical_index = str(row) + " "
            if row < 10:
                vertical_index += " "
            vertical_index += " "
            result += vertical_index + "  ".join(self.__board[row]) + " \n"
        return result

    def databse_format(self):
        result = self.__players[0].sign
        for row in self.__board:
            result += '|' + ",".join(row)
        return result
