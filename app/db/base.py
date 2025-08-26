# This file is used to create a Declarative Base for SQLAlchemy models.
# By importing this Base into your model files, Alembic and other tools
# can discover all the models that should be included in database migrations.

from sqlalchemy.orm import declarative_base

# The declarative_base() function returns a new base class from which all
# mapped classes should inherit. When the class definition is completed, a new

# Table and mapper() will have been generated.
Base = declarative_base()
