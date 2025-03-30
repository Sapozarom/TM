from src.model.game import Game
from src.model.player import Player
from src.model.generation import Generation
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class UpdateDbTables():
    engine = create_engine("sqlite:///tmdb.db", echo=True)

    object_list: list

    def create_new_game(self, game: Game):
        with Session(self.engine) as session:
            session.add_all([game])
            session.commit()
