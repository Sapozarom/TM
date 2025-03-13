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


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    terraforming_rating: Mapped[int] = mapped_column()
    number: Mapped[int] = mapped_column()
