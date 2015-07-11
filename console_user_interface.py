from game import Game
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from create_db import User
from getpass import getpass


######
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
    print(prompt)
    choice = input("Your choice: ")
    while(choice not in options):
        print("There is no such option. Try again!")
        choice = input("Your choice: ")
    options[choice](session)


def sign_in(session):
    username = input("Username: ")
    user = session.query(User).filter(User.name == username).all()
    if user:
        password = getpass("Password: ")
        if user[0].password == password:
            if user[0].unfinished_game_mode in ["easy", "hard"]:
                load_game(session, user[0])
            else:
                main_menu(session, user[0])
        else:
            print("Invalid password. Try again.")
            start_menu(session)
    else:
        print("There isn't registered such user. Register?")
        start_menu(session)


def register(session):
    username = input("Username: ")
    is_name_taken = session.query(User).filter(User.name == username).all()
    while(is_name_taken):
        print("There is already a user with such name. Try another:)")
        username = input("Username: ")
        is_name_taken = session.query(User).filter(User.name == username).all()
    password = getpass("Please, type your password: ")
    password_conformation = getpass("Please, confirm your password: ")
    while(password != password_conformation):
        print("There is some mistake. Try again!")
        password = getpass("Please, type your password: ")
        password_conformation = getpass("Please, confirm your password: ")
    new_user = User(name=username, password=password,
                    wins_easy_level=0, losses_easy_level=0,
                    wins_hard_level=0, losses_hard_level=0,
                    unfinished_game_board="none",
                    unfinished_game_mode="none")
    session.add(new_user)
    session.commit()
    print("Successful registration! Please, sign in:\n")
    sign_in(session)


######
def main_menu(session, user=None):
    options = {"new_game": take_user_game_setup,
               "score_board": score_board,
               "exit": close_database
               }
    prompt = ("\nMain menu:" +
              "\n new_game -> to start a game" +
              "\n score_board -> to see the top 3 players" +
              "\n exit -> to quit\n")
    print(prompt)
    choice = input("Your choice: ")
    while(choice not in options):
        print("There is no such option. Try again!")
        choice = input("Your choice: ")
    options[choice](session, user)


###
def take_user_game_setup(session, user, *args):
    board_size = int(input("Board size: "))
    while (board_size < 4) or (16 < board_size):
        print("The size should be between 4 and 16.")
        board_size = int(input("Board size: "))
    start_stones = int(input("Start number of stones: "))
    while (start_stones != 1) and (start_stones % board_size != 0):
        print("Number of stones could be 1 or divisible by the board size.")
        start_stones = int(input("Start number of stones: "))
    mode = input("Choose 'easy' or 'hard' mode: ")
    while mode not in ["easy", "hard"]:
        print("There is no such option.")
        mode = input("Mode: ")
    players_signs = ["X", "O"]
    user_sign = input("Choose 'X' or 'O' as a sign: ")
    while user_sign not in players_signs:
        print("There is no such option.")
        user_sign = input("Sign: ")
    players_signs.remove(user_sign)
    computer_sign = players_signs[0]
    board = None
    game = Game(user_sign, computer_sign, mode,
                board_size, board, start_stones)
    start_game(session, user, game)


def load_game(session, user):
    mode = user.unfinished_game_mode
    board_information = user.unfinished_game_board.split('|')
    user_sign = board_information[0]
    signs = ["X", "O"]
    signs.remove(user_sign)
    computer_sign = signs[0]
    board_size = len(board_information) - 1
    board = board_information[1:]

    start_stones = None
    game = Game(user_sign, computer_sign, mode,
                board_size, board, start_stones)
    start_game(session, user, game)
###


def score_board(session, user):
    print("\nTop 3 players:")
    all_users = session.query(User).all()
    sorted(all_users, key=lambda user: (user.wins_hard_level,
                                        user.wins_easy_level))
    count = 0
    while count < 3 and count < len(all_users):
        print(str(count + 1) + " " + score_board_format(all_users[count]))
        count += 1

    input("Press Enter to return to Main menu")
    main_menu(session, user)


def score_board_format(user):
    hard_mode = "\nhard mode wins/losses: {}/{}".format(user.wins_hard_level,
                                                        user.losses_hard_level)
    easy_mode = "\neasy mode wins/losses: {}/{}".format(user.wins_easy_level,
                                                        user.losses_easy_level)
    return user.name + hard_mode + easy_mode


######
def start_game(session, user, game):

    options = {"new_game": take_user_game_setup,
               "save_and_exit": save_and_exit,
               "exit": close_database,
               "main_menu": main_menu
               }
    user_prompt = ("\nDuring the game, you could start 'new_game'," +
                   " 'save_and_exit' or 'exit' at any time")
    guest_prompt = ("\nDuring the game, you could start 'new_game'" +
                    " or 'exit' at any time")
    if user:
        print(user_prompt)
    else:
        print(guest_prompt)

    print("\nSTART BOARD\n" + str(game.board) + "\n")
    command = None
    continue_game = True
    while continue_game:
        print("Your turn!")
        pick = input("Pick stone (row, col): ")
        if pick in options:
            command = pick
            break
        move = input("Move to (row, col): ")
        if move in options:
            command = move
            break
        pick = pick[1:-1].split(", ")
        from_row = int(pick[0])
        from_col = int(pick[1])
        move = move[1:-1].split(", ")
        to_row = int(move[0])
        to_col = int(move[1])
        game.play_user_turn(from_row, from_col, to_row, to_col)
        print("YOUR MOVE:\n" + str(game.board))
        game.play_computer_turn()
        print("\nCOMPUTER MOVE:\n" + str(game.board))
        continue_game = game.running

    if command:
        options[command](session, user, game)
    else:
        if user:
            if user.unfinished_game_mode in ["easy", "hard"]:
                user.unfinished_game_mode = "none"
                user.unfinished_game_board = "none"
            if game.does_user_win:
                print("Congratulations you win!")
                if game.mode == "easy":
                    user.wins_easy_level += 1
                else:
                    user.wins_hard_level += 1
            elif game.does_user_win is None:
                print("Equal game! Won't be signed in the database!")
            else:
                print("You lose!")
                if game.mode == "hard":
                    user.losses_hard_level += 1
                else:
                    user.losses_easy_level += 1
            session.commit()
        else:
            if game.does_user_win:
                print("Congratulations you win!")
            elif game.does_user_win is None:
                print("Equal game!")
            else:
                print("You lose!")

        go_to = input("Go to 'main_menu' or 'exit': ")
        while go_to not in ["main_menu", "exit"]:
            print("There is no such option.")
            go_to = input("Your choice: ")
        options[go_to](session, user)


def save_and_exit(session, user, game):
    if user:
        user.unfinished_game_mode = game.mode
        user.unfinished_game_board = game.board.database_format()
        session.commit()
    else:
        print("Guests can't save games!")
    close_database(session)


def close_database(session, *args):
    session.close()


def main():
    engine = create_engine("sqlite:///users.db")
    session = Session(bind=engine)
    start_menu(session)

if __name__ == '__main__':
    main()
