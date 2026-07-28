from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from etl.config import get_settings


def create_database_engine() -> Engine:
    """Create a synchronous SQLAlchemy engine for the configured database."""
    settings = get_settings()

    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
    )


engine = create_database_engine()

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
