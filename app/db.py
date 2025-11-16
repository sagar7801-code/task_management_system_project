from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite file - will be created in project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"


# connect_args required for SQLite to allow multi-threading in dev server
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
