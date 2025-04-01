import sys

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
if TYPE_CHECKING:
    from src.model.game import Game


class Base(DeclarativeBase):
    pass


class Generation(Base):
    __tablename__ = 'generation'
    __allow_unmapped__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column()
    game: Mapped["Game"] = relationship(back_populates="generation")
    # game = Game

    # [player_number=> [list of cards]]
    reserch_phase: dict
