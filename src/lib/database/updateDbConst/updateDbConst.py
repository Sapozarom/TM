from src.model.game import Game
from src.model.player import Player
from src.model.generation import Generation
from src.model.corporation import Corporation
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class UpdateDbConst():
    engine = create_engine("sqlite:///tmdb.db", echo=True)

    object_list: list

    def main(self):
        B_03 = Corporation()
        B_03.id = 4
        B_03.exp = "Base"
        B_03.name = "Helion"
        B_03.bottom_text = "You start with 3 heat production and 42 M€."

        B_03.top_text = "Effect: You may use heat as M€. You may not use M€ as heat."
        B_03.picto = ""
        B_03.mega_credits = 42
        B_03.t_wild = 1

        B_08 = Corporation()
        B_08.id = 13
        B_08.exp = "Base"
        B_08.name = "Tharsis Republic"
        B_08.bottom_text = "You start with 40 M€. As your first action in the game, place a city tile."
        B_08.top_text = "Effect: When any city tile is placed ON MARS, increase your M€ production 1 step. When you place a city tile, gain 3 M€."
        B_08.picto = ""
        B_08.mega_credits = 42
        B_08.t_building = 1

        PC_1 = Corporation()
        PC_1.id = 14
        PC_1.exp = "Prelude"
        PC_1.name = "Cheung Shing Mars"
        PC_1.bottom_text = "You start with 44 M€ and 3 M€ production."
        PC_1.top_text = "Effect: When you play a building tag, you pay 2 M€ less for it."
        PC_1.picto = ""
        PC_1.mega_credits = 44
        PC_1.t_building = 1

        # corp = [B_03, B_08, PC_1]

        with Session(self.engine) as session:
            session.add_all([B_03, B_08, PC_1])
            session.commit()
