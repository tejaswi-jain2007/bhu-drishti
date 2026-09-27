import os
import pathlib
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger("nwis.database")

def get_database_engine():
    db_url = settings.DATABASE_URL
    
    # Check if PostgreSQL is specified, try connecting
    if db_url.startswith("postgresql"):
        try:
            test_engine = create_engine(db_url, echo=False, pool_pre_ping=True)
            with test_engine.connect():
                logger.info("Connected to PostgreSQL database successfully.")
                return test_engine
        except Exception as e:
            logger.warning(
                f"PostgreSQL connection failed ({e}). "
                "Falling back to local SQLite database (nwis.db)."
            )
            # Find local SQLite database path
            possible_paths = [
                os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/nwis.db")),
                os.path.abspath("data/nwis.db"),
                os.path.abspath("../data/nwis.db"),
                os.path.abspath("backend/data/nwis.db"),
            ]
            sqlite_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    sqlite_path = p
                    break
            
            if not sqlite_path:
                sqlite_path = possible_paths[0]
                os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
            
            posix_path = pathlib.Path(sqlite_path).as_posix()
            sqlite_url = f"sqlite:///{posix_path}"
            return create_engine(
                sqlite_url,
                connect_args={"check_same_thread": False},
                echo=False
            )
    else:
        connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
        return create_engine(db_url, connect_args=connect_args, echo=False)

engine = get_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
