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

    def __repr__(self):
        return f"Player {self.number}\n" \
            f"TR: {self.terraforming_rating}\n" \
            f"Mega Credit: {self.mega_credit} with production {self.mega_credit_prod}\n" \
            f"Steel: {self.steel} with production {self.steel_prod}\n" \
            f"Titanium: {self.titanium} with production {self.titaniu_prod}\n" \
            f"Plant: {self.plant} with production {self.plant_prod}\n" \
            f"Energy: {self.energy} with production {self.energy_prod}\n" \
            f"Heat: {self.heat} with production {self.heat_prod}\n"
