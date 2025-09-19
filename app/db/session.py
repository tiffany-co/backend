from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# Create a SQLAlchemy engine instance.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker class, a factory for creating new Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class.
# All ORM models will inherit from this class. It's defined here to be the
# single source of truth and avoid circular import issues.
Base = declarative_base()