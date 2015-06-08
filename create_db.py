from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    name = Column(String, primary_key=True)
    password = Column(String)
    wins_easy_level = Column(Integer)
    losses_easy_level = Column(Integer)
    wins_hard_level = Column(Integer)
    losses_hard_level = Column(Integer)
    unfinished_game_board = Column(postgresql.ARRAY(String))
    unfinished_game_mode = Column(String)


engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)
