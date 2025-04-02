import sys

from typing import List
from typing import Dict
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


class Generation(ModelBase):
    __tablename__ = 'generation'
    __allow_unmapped__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column()
    game: Mapped["Game"] = relationship(back_populates="generations")
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    # game = Game

    # [player_number => [list of cards]]
    reserch_phase_str: Mapped[str] = mapped_column()

    reserch_phase_dict: dict = {}

    def __init__(self, number, **kw):
        self.number = number
        super().__init__(**kw)
