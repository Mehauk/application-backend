from sqlmodel import Session, create_engine
from ..config.database import DatabaseSettings

engine = create_engine(
    DatabaseSettings().database_url,
    connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session
