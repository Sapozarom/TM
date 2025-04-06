# from src.model.game import Game
# from src.model.player import Player
# from src.model.generation import Generation
# from src.model.corporation import Corporation
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING
from src.model.corporation import Corporation

# if TYPE_CHECKING:


class GetFromDb():
    engine = create_engine("sqlite:///tmdb.db", echo=True)

    def getCorporationById(self, corp_id):
        corp = None
        # session = Session(self.engine)

        stmt = select(Corporation).where(Corporation.id == corp_id)

        # print(stmt)

        with Session(self.engine) as conn:
            result = conn.execute(stmt).one()
            # print(result[0])
            if isinstance(result[0], Corporation):
                corp = result[0]

        return corp
