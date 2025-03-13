import sys
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base = declarative_base()


Base = declarative_base()


class Game(Base):

    __tablename__ = "games"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    start_time = Column('start_time', String)
    map = Column("map", String)

    def __init__(self, start_time, map):

        # self.id =
        self.start_time = start_time
        self.map = map


engine = create_engine("sqlite:///tmdb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

new_game = Game("dziś", "Tharsis")

session.add(new_game)
session.commit
