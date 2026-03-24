from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------------
# Database Configuration
# ---------------------------------

# Using SQLite for development (simple & no setup)
DATABASE_URL = "sqlite:///./hospital.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()


# ---------------------------------
# Database Dependency
# ---------------------------------
def get_db():
    """
    Creates a new database session for each request
    and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
