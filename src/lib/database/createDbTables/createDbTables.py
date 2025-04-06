from src.model.game import Game
from src.model.player import Player
from src.model.generation import Generation
from src.model.corporation import Corporation
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class CreateDbTables():

    def main(self):
        engine = create_engine("sqlite:///tmdb.db", echo=True)
        Game.metadata.create_all(engine)
        Player.metadata.create_all(engine)
        Generation.metadata.create_all(engine)
        Corporation.metadata.create_all(engine)

    if __name__ == "__main__":
        main()
