
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
    from src.model.player import Player


class Corporation(ModelBase):
    __tablename__ = 'corporation'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    exp: Mapped[str] = mapped_column(String(30))
    bottom_text: Mapped[str] = mapped_column(String(200))
    top_text: Mapped[str] = mapped_column(String(200))
    picto: Mapped[str] = mapped_column(String(200))
    mega_credits: Mapped[int] = mapped_column()

    players: Mapped[List["Player"]] = relationship(
        back_populates="corporation", cascade="all, delete-orphan")

    # tags [b, c, s, po, pl, m, a, e, j, v, w]
    t_building: Mapped[int] = mapped_column()
    t_city: Mapped[int] = mapped_column()
    t_space: Mapped[int] = mapped_column()
    t_power: Mapped[int] = mapped_column()
    t_plant: Mapped[int] = mapped_column()
    t_microbe: Mapped[int] = mapped_column()
    t_animal: Mapped[int] = mapped_column()
    t_earth: Mapped[int] = mapped_column()
    t_jovian: Mapped[int] = mapped_column()
    t_venus: Mapped[int] = mapped_column()
    t_wild: Mapped[int] = mapped_column()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.t_building = 0
        self.t_city = 0
        self.t_space = 0
        self.t_power = 0
        self.t_plant = 0
        self.t_microbe = 0
        self.t_animal = 0
        self.t_earth = 0
        self.t_jovian = 0
        self.t_venus = 0
        self.t_wild = 0

    # Everything = -1,
    # None = 0,
    # Beginner = 1,
    # Inventrix = 2,
    # PhoboLob = 3,
    # Helion = 4,
    # Teractor = 5,
    # SaturnSystems = 6,
    # UNMI = 7,
    # InterplanetaryCinematics = 8,
    # Credicor = 9,
    # Thorgate = 10,
    # MiningGuild = 11,
    # Ecoline = 12,
    # TharsisRepublic = 13,
    # CheungShingMars = 14,
    # PointLuna = 15,
    # RobinsonIndustries = 16,
    # ValleyTrust = 17,
    # Vitor = 18,
    # Aphrodite = 19,
    # Manutech = 20,
    # Viron = 21,
    # MorningStarInc = 22,
    # Celestic = 23,
    # Splice = 24,
    # Recyclon = 25,
    # ArcadianCommunities = 26,
    # PharmacyUnion_Event = 29,
    # PharmacyUnion = 30,
    # Astrodrill = 31
