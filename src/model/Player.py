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

    def __init__(self, **kw):
        super().__init__(**kw)
