from game import Game
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# some help functions here

def main():
    user = None
    game = Game()
    continue_game = True

    engine = create_engine("sqlite:///users.db")
    session = Session(bind=engine)

    # take input to login user or set it as guest
    # show scoreboard if user wants
    # setup game
    # while continue_game is true:
    #   print game.board
    #   get user's move coordinates
    #   if not "exit", "new game" or "save and exit":
    #     continue_game = game.play_user_turn()
    #     print game.board
    # otherwise write status to DB
    # output result
    # close DB session
    pass

if __name__ == '__main__':
    main()
