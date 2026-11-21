from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


database_url = settings.database_url
engine_options = {"pool_pre_ping": True}
if make_url(database_url).get_backend_name() == "sqlite":
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
