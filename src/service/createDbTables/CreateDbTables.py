from src.model.game import Game
from src.model.player import Player
from src.model.generation import Generation
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# import sys
# raise RuntimeError(sys.path)

# pip install src


class CreateDbTables():

    def main(self):
        engine = create_engine("sqlite:///tmdb.db", echo=True)
        Game.metadata.create_all(engine)
        Player.metadata.create_all(engine)
        Generation.metadata.create_all(engine)

    if __name__ == "__main__":
        main()
