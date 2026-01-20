from sqlmodel import create_engine, Session
from ..config import settings


# Create the database engine
engine = create_engine(
    settings.NEON_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=0,
)


def get_database_session():
    """
    Dependency to get a database session.
    This provides the database connection service as required by the constitution.
    """
    with Session(engine) as session:
        yield session