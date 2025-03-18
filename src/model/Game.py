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
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start: Mapped[str] = mapped_column(String(30))
    players: Mapped[List["Player"]] = relationship(
        back_populates="game", cascade="all, delete-orphan")

    # Phase of the game tweak how some parts of events work
    # current phases are
    # 0 - NOT_STARTED - before game was created and after it was finished
    # 1 = GAME_INITIALIZATION - part when players and board setup is created
    phase = "NOT_STARTED"

    # object of player who currently takes action
    current_player: Player = None

    # number of player who currently takes action
    __current_player_number = 0

    @property
    def number_of_players(self):
        return len(self.players)

    @property
    def current_player_number(self):
        return self.__current_player_number

    @current_player_number.setter
    def current_player_number(self, number):
        if 0 < number <= self.number_of_players:
            self.__current_player_number = number

            if self.players[number-1].number == number:
                self.current_player = self.players[number-1]
            else:
                self.current_player = next(
                    (x for x in self.players if x.number == number), None)
        else:
            self.__current_player_number = 0
            self.current_player = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_player_number = 0

    def add_player(self, number):
        new_player = Player()
        new_player.number = number
        self.players.append(new_player)

    # def
