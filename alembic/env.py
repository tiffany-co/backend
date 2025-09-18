import sys
from logging.config import fileConfig
from pathlib import Path

# --- Add project root to Python path ---
# This ensures that Alembic can find the 'app' module.
root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))
# ---

from sqlalchemy import engine_from_config, pool
import sqlalchemy as sa

from alembic import context

# --- Import settings and the declarative Base ---
from app.core.config import settings
# This is the crucial change: import Base from its correct location.
from app.db.session import Base
# Import all models here so that Alembic can see them and autogenerate migrations.
from app.db.base import * # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate support.
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Set the sqlalchemy.url in the config object programmatically from our settings
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            sql_script_path = Path(__file__).parent / "sql" / "cap_audit_log.sql"
            if sql_script_path.is_file():
                connection.execute(sa.text(sql_script_path.read_text()))
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

