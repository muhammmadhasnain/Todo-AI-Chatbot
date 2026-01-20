# from sqlmodel import create_engine, Session, SQLModel
# from ..config import settings

# engine = create_engine(
#     settings.NEON_DATABASE_URL,
#     echo=settings.DEBUG,
#     pool_pre_ping=True,
#     pool_size=5,        # Neon pooler friendly
#     max_overflow=0,     # IMPORTANT: pooler ke sath overflow mat rakho
#     pool_recycle=300,   # Recycle connections after 5 minutes
#     pool_timeout=30,    # Connection timeout
#     connect_args={
#         "options": "-c statement_timeout=30000",  # 30 second statement timeout
#         "keepalives_idle": 30,
#         "keepalives_interval": 5,
#         "keepalives_count": 3
#     }
# )

# def get_session():
#     with Session(engine) as session:
#         yield session

# def create_tables():
#     """
#     Create all database tables based on models.
#     NOTE: Excludes the User table since it's managed by Better Auth.
#     """
#     # Get all models except User to avoid conflicts with Better Auth
#     from ..models.user import User
#     from ..models.task import Task
#     from ..models.conversation import Conversation
#     from ..models.message import Message

#     # Create tables for all models except User (which is handled by Better Auth)
#     # We'll use SQLModel's metadata but exclude the User table
#     # Create a new metadata object with only the tables we want
#     from sqlmodel import SQLModel
#     from sqlalchemy import MetaData

#     # Create tables for non-user models only
#     Task.metadata.create_all(engine, checkfirst=True)
#     Conversation.metadata.create_all(engine, checkfirst=True)
#     Message.metadata.create_all(engine, checkfirst=True)





# # from sqlmodel import create_engine, Session, SQLModel
# # from ..config import settings
# # import os

# # # Use the appropriate database URL based on environment


# # # Create the engine with appropriate settings for Neon compatibility
# # engine = create_engine(
# #     settings.NEON_DATABASE_URL,
# #     echo=settings.DEBUG,  # Log SQL queries in debug mode
# #     pool_pre_ping=True,   # Verify connections before use
# #     pool_recycle=300,     # Recycle connections after 5 minutes
# #     pool_size=5,          # Reduced pool size for Neon compatibility
# #     max_overflow=10,      # Allow additional connections when needed
# #     pool_timeout=30,      # Connection timeout
# #     connect_args={
# #         # Neon-specific connection arguments for pooled connections
# #         "options": "-c statement_timeout=30000"  # 30 second statement timeout
# #     }
# # )

# # def get_session():
# #     """Dependency to get a database session."""
# #     with Session(engine) as session:
# #         yield session

# # def create_tables():
# #     """Create all database tables based on models."""
# #     SQLModel.metadata.create_all(engine)


from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import MetaData
from ..config import settings

engine = create_engine(
    settings.NEON_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,        # Neon pooler friendly
    max_overflow=0,     # ✅ correct for pooler
    pool_recycle=300,   # recycle stale connections
    pool_timeout=30     # connection wait timeout
)

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    """
    Create all database tables based on models.
    NOTE: Includes the User Profile table for application-specific user data.
    Better Auth manages the core user authentication data separately.
    """
    # Import models to ensure they are registered with SQLModel metadata
    from ..models.user import User
    from ..models.task import Task
    from ..models.conversation import Conversation
    from ..models.message import Message

    # Create tables for all models including User Profile (application-specific user data)
    # Better Auth handles authentication, but we maintain our own user profile table
    User.metadata.create_all(engine, checkfirst=True)
    Task.metadata.create_all(engine, checkfirst=True)
    Conversation.metadata.create_all(engine, checkfirst=True)
    Message.metadata.create_all(engine, checkfirst=True)
