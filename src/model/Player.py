from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from src.model.modelBase import ModelBase

if TYPE_CHECKING:
    from src.model.game import Game


# class Base(DeclarativeBase):
#     pass


class Player(ModelBase):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    game: Mapped["Game"] = relationship(back_populates="players")
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    terraforming_rating: Mapped[int] = mapped_column()
    number: Mapped[int] = mapped_column()

    mega_credit = 0
    steel = 0
    titanium = 0
    plant = 0
    energy = 0
    heat = 0

    mega_credit_prod = 0
    steel_prod = 0
    titaniu_prod = 0
    plant_prod = 0
    energy_prod = 0
    heat_prod = 0

    def __init__(self, **kw):
        super().__init__(**kw)
