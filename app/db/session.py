from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine.
# The engine is the starting point for any SQLAlchemy application. It's the
# 'home base' for the actual database and its DBAPI, delivered to the SQLAlchemy
# application through a connection pool.
# pool_pre_ping=True checks for "stale" connections before they are used.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker.
# This is a factory for creating new Session objects. It's configured with
# the engine and other options. When we need a database session in our
# application, we will instantiate this.
# autocommit=False: Changes are not committed automatically. We must explicitly call db.commit().
# autoflush=False: Changes are not flushed to the DB automatically.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
