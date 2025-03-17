import sys


from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from src.model.player import Player
from src.model.generation import Generation
from src.model.modelBase import ModelBase

# class Base(DeclarativeBase):
#     pass


class Game(ModelBase):
    __tablename__ = 'game'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start: Mapped[str] = mapped_column(String(30))
    players: Mapped[List["Player"]] = relationship(
        back_populates="game", cascade="all, delete-orphan")

    # Phase of the game tweak how some parts of events work
    # current phases are
    # 0 - NOT_STARTED - before game was created and after it was finished
    # 1 = GAME_INITIALIZATION - part when players and board setup is created
    phase = "NOT_STARTED"

    # number of player who currently takes action
    current_player = 0

    def __init__(self, **kw):
        super().__init__(**kw)

    def add_player(self, number):
        new_player = Player()
        new_player.number = number
        self.players.append(new_player)

    @property
    def number_of_players(self):
        return len(self.players)
