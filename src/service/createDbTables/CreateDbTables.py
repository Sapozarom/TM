from src.model.Game import Game
from src.model.Player import Player
from src.model.Generation import Generation
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# import sys
# raise RuntimeError(sys.path)

# pip install src


class CreateDbTables():

    def create(self):
        engine = create_engine("sqlite:///tmdb.db", echo=True)
        Game.metadata.create_all(engine)
        Player.metadata.create_all(engine)
        Generation.metadata.create_all(engine)

    # if __name__ == "__main__":
    #     main()


# class CreateDbTables():
#     engine = create_engine("sqlite:///tmdb.db", echo=True)
#     # Game.metadata.create_all(engine)
#     # Player.metadata.create_all(engine)
#     # Generation.metadata.create_all(engine)
