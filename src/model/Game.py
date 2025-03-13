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


class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = 'game'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start: Mapped[str] = mapped_column(String(30))


# engine = create_engine("sqlite:///tmdb.db", echo=True)
# # Base.metadata.create_all(engine)

# session = Session(engine)

# ng = Game(
#     # id=1,
#     start='dziś'
# )

# session.add_all([ng])
# session.commit()
