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

    # General
    game_id: str
    game_seed: str = None
    is_custom: bool = None
    is_online: bool = None
    is_draft: bool = None
    is_ranked: bool = None
    # Data
    variant: str = None
    prelude_phase: bool = None
    tr_63: bool = None
    board_type: str = None
    beginner_corp: bool = None
    extension_cards: List = None
    extension_corps: List = None
    corp_separate_draw: bool = None
    generation_level: int = None
    # Global parameters:

    temperature_level: int = None
    oxygen_level: int = None
    ocean_level: int = None
    venus_scale: int = None
    # Setup
    is_player_replaced_by_aI: bool
    is_player_order_shuffled: bool

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

    @property
    def has_current_player(self):
        value = False

        if not (self.current_player == None) and (isinstance(self.current_player, Player)):
            value = True

        return value

    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_player_number = 0

    def add_player(self, number):
        new_player = Player()
        new_player.number = number
        self.players.append(new_player)

    # def
    def print_game_setup(self):
        print(f"### GENERAL ###")
        print(f"Game with GameID: -{self.game_id}-")
        print(f"Seed: -{self.game_seed}-")
        print(f"is custom: -{self.is_custom}-")
        print(f"Is online: -{self.is_online}-")
        print(f"Is draft: -{self.is_online}-")
        print(f"Is draft: -{self.is_draft}-")
        print(f"Is ranked: -{self.is_ranked}-")
        print(f"Is online: -{self.is_online}-")
        print(f"### DATA ###")
        print(f"Variant: -{self.variant}-")
        print(f"Prelude phase: -{self.prelude_phase}-")
        print(f"TR 63: -{self.tr_63}-")
        print(f"Boadr type: -{self.board_type}-")
        print(f"Beginner Corp: -{self.beginner_corp}-")
        print(f"Extension Cards: ")
        for extension in self.extension_cards:
            print(f"---- -{extension}-")
        print(f"Extension Corps: ")
        for extension in self.extension_corps:
            print(f"---- -{extension}-")
        print(f"Generation: |{self.generation_level}|")
        print(f"### GLOBAL PARAMETERS ###")
        print(f"Temperature: |{self.temperature_level} deg. C|")
        print(f"Oxygen: |{self.oxygen_level}%|")
        print(f"Oceans: |{self.ocean_level}|")
        print(f"Venus Scale: |{self.venus_scale}%|")
