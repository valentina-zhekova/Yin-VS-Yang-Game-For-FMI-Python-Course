from game import Game
from console_user_interface import take_user_choice, user_input, output_prompt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from create_db import User
from getpass import getpass
import re


def start_menu(session):
    options = {"sign_in": sign_in,
               "register": register,
               "guest": main_menu,
               "exit": close_database
               }
    prompt = ("\nWelcome, please choose:" +
              "\n sign_in -> to use your account" +
              "\n register -> to make an account" +
              "\n guest -> to play as guest" +
              "\n exit -> to quit\n")
    wait_prompt = "Your choice: "
    error_prompt = "There is no such option. Try again!"

    def condition(x): return x in options
    choice = take_user_choice(condition, wait_prompt, error_prompt, prompt)
    options[choice](session)


def sign_in(session):
    username = user_input("Username: ")
    user = session.query(User).filter(User.name == username).all()
    if user:
        password = getpass("Password: ")
        if user[0].password == password:
            if user[0].unfinished_game_mode in ["easy", "hard"]:
                load_game(session, user[0])
            else:
                main_menu(session, user[0])
        else:
            output_prompt("Invalid password. Try again.")
            start_menu(session)
    else:
        output_prompt("There isn't registered such user. Register?")
        start_menu(session)


def register(session):
    def condition1(x):
        users = session.query(User).filter(User.name == x).all()
        return not users
    wait_prompt1 = "Username: "
    error_prompt1 = "There is already a user with such name. Try another:)"
    username = take_user_choice(condition1, wait_prompt1, error_prompt1)

    def condition2(x):
        return getpass("Confirm password: ") == x
    wait_prompt2 = "Please, type your password: "
    error_prompt2 = "There is some mistake. Try again!"
    password = take_user_choice(condition2, wait_prompt2, error_prompt2,
                                function=getpass)

    add_new_user(session, username, password)
    output_prompt("Successful registration! Please, sign in:\n")
    sign_in(session)


def add_new_user(session, username, password):
    new_user = User(name=username, password=password,
                    wins_easy_level=0, losses_easy_level=0,
                    wins_hard_level=0, losses_hard_level=0,
                    unfinished_game_board="none",
                    unfinished_game_mode="none")
    session.add(new_user)
    session.commit()


def main_menu(session, user=None):
    options = {"new_game": take_user_game_setup,
               "score_board": score_board,
               "exit": close_database
               }
    prompt = ("\nMain menu:" +
              "\n new_game -> to start a game" +
              "\n score_board -> to see the top 3 players" +
              "\n exit -> to quit\n")

    def condition(x):
        return x in options
    wait_prompt = "Your choice: "
    error_prompt = "There is no such option. Try again!"
    choice = take_user_choice(condition, wait_prompt, error_prompt, prompt)
    options[choice](session, user)


def take_user_game_setup(session, user, *args):
    def condition1(x):
        pattern = re.compile("[\d{1, 2}]")
        return pattern.match(x) and (4 <= int(x)) and (int(x) <= 16)
    wait_prompt1 = "Board size: "
    error_prompt1 = "The size should be between 4 and 16."
    size = int(take_user_choice(condition1, wait_prompt1, error_prompt1))

    def condition2(x):
        pattern = re.compile("[\d{1, 2}]")
        return pattern.match(x) and (int(x) == 1) or (int(x) % size == 0)
    wait_prompt2 = "Start number of stones: "
    error_prompt2 = "Number of stones could be 1 or divisible by board size."
    start_stones = int(take_user_choice(condition2, wait_prompt2,
                                        error_prompt2))

    def condition3(x):
        return x in ["easy", "hard"]
    wait_prompt3 = "Mode 'easy' or 'hard': "
    error_prompt3 = "There is no such option."
    mode = take_user_choice(condition3, wait_prompt3, error_prompt3)

    def condition4(x):
        return x in ["X", "O"]
    wait_prompt4 = "Sign 'X' or 'O': "
    error_prompt4 = "There is no such option."
    user_sign = take_user_choice(condition4, wait_prompt4, error_prompt4)
    computer_sign = find_opponent_sign(user_sign)

    board = None
    game = Game(user_sign, computer_sign, mode, size, board, start_stones)
    start_game(session, user, game)


def find_opponent_sign(player_sign):
    players_signs = ["X", "O"]
    players_signs.remove(player_sign)
    return players_signs[0]


def load_game(session, user):
    mode = user.unfinished_game_mode
    board_information = user.unfinished_game_board.split('|')
    user_sign = board_information[0]
    computer_sign = find_opponent_sign(user_sign)
    size = len(board_information) - 1
    board = board_information[1:]
    start_stones = None
    game = Game(user_sign, computer_sign, mode, size, board, start_stones)
    start_game(session, user, game)


def score_board(session, user):
    output_prompt("\nTop 3 players:")
    all_users = session.query(User).all()
    sorted(all_users, key=lambda user: (user.wins_hard_level,
                                        user.wins_easy_level))
    count = 0
    while count < 3 and count < len(all_users):
        output_prompt(str(count + 1) + " " +
                      score_board_format(all_users[count]))
        count += 1

    user_input("Press Enter to return to Main menu")
    main_menu(session, user)


def score_board_format(user):
    hard_mode = "\nhard mode wins/losses: {}/{}".format(user.wins_hard_level,
                                                        user.losses_hard_level)
    easy_mode = "\neasy mode wins/losses: {}/{}".format(user.wins_easy_level,
                                                        user.losses_easy_level)
    return user.name + hard_mode + easy_mode


def start_game(session, user, game):
    options = {"new_game": take_user_game_setup,
               "save_and_exit": save_and_exit,
               "exit": close_database
               }
    user_prompt = ("\nDuring the game, you could start 'new_game'," +
                   " 'save_and_exit' or 'exit' at any time")
    guest_prompt = ("\nDuring the game, you could start 'new_game'" +
                    " or 'exit' at any time")
    if user:
        output_prompt(user_prompt)
    else:
        output_prompt(guest_prompt)

    output_prompt("\nSTART BOARD\n" + str(game.board))
    command = None
    continue_game = True
    while continue_game:
        output_prompt("\nYour turn!")
        choice = take_user_move()
        if choice in options:
            command = choice
            break
        else:
            from_row, from_col, to_row, to_col = choice
        successful = game.play_user_turn(from_row, from_col, to_row, to_col)
        while (not successful) or (choice in options):
            choice = take_user_move()
            if choice in options:
                command = choice
                break
            else:
                from_row, from_col, to_row, to_col = choice
            successful = game.play_user_turn(from_row, from_col,
                                             to_row, to_col)
        if command:
            break
        else:
            output_prompt("YOUR MOVE:\n" + str(game.board))
            game.play_computer_turn()
            output_prompt("\nCOMPUTER MOVE:\n" + str(game.board))
            continue_game = game.running

    if command:
        options[command](session, user, game)
    else:
        game_finished(session, user, game)


def take_user_move():
    def condition(x):
        pattern = re.compile("[\(\d{1, 2}, \d{1, 2}\)]")
        return pattern.match(x) or (x in ["exit", "save_and_exit", "new_game"])
    error_prompt = "Not a valid input."
    pick = take_user_choice(condition, "Pick stone (row, col): ", error_prompt)
    if pick in ["exit", "save_and_exit", "new_game"]:
        return pick
    move = take_user_choice(condition, "Move to (row, col): ", error_prompt)
    if move in ["exit", "save_and_exit", "new_game"]:
        return pick
    pick = pick[1:-1].split(", ")
    move = move[1:-1].split(", ")
    from_row, from_col = int(pick[0]), int(pick[1])
    to_row, to_col = int(move[0]), int(move[1])
    return (from_row, from_col, to_row, to_col)


def game_finished(session, user, game):
    options = {"exit": close_database,
               "main_menu": main_menu
               }
    if user:
        if user.unfinished_game_mode in ["easy", "hard"]:
            user.unfinished_game_mode = "none"
            user.unfinished_game_board = "none"
        if game.does_user_win:
            output_prompt("Congratulations you win!")
            if game.mode == "easy":
                user.wins_easy_level += 1
            else:
                user.wins_hard_level += 1
        elif game.does_user_win is None:
            output_prompt("Equal game! Won't be signed in the database!")
        else:
            output_prompt("You lose!")
            if game.mode == "hard":
                user.losses_hard_level += 1
            else:
                user.losses_easy_level += 1
        session.commit()
    else:
        if game.does_user_win:
            output_prompt("Congratulations you win!")
        elif game.does_user_win is None:
            output_prompt("Equal game!")
        else:
            output_prompt("You lose!")

    def condition(x): return x in ["main_menu", "exit"]
    wait_prompt = "Go to 'main_menu' or 'exit': "
    error_prompt = "There is no such option."
    go_to = take_user_choice(condition, wait_prompt, error_prompt)
    options[go_to](session, user)


def save_and_exit(session, user, game):
    if user:
        user.unfinished_game_mode = game.mode
        user.unfinished_game_board = game.board.database_format()
        session.commit()
    else:
        output_prompt("Guests can't save games!")
    close_database(session)


def close_database(session, *args):
    session.close()


def main():
    engine = create_engine("sqlite:///users.db")
    session = Session(bind=engine)
    start_menu(session)

if __name__ == '__main__':
    main()
