from contextlib import contextmanager
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

from .models import *  # noqa: F401,F403

SQLITE_URL = "sqlite:///./logistics.db"
engine = create_engine(SQLITE_URL, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# FastAPI dependency style
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
