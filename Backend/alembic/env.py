from logging.config import fileConfig
from os import environ

from dotenv import dotenv_values
from sqlalchemy import create_engine

from alembic import context
from models.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

if production := environ.get("PRODUCTION", False):
    host = environ.get("DB_HOST")
    port = environ.get("DB_PORT", 5432)
    username = environ.get("DB_USER")
    password = environ.get("DB_PASSWORD")
    database = environ.get("DB_NAME")
else:
    config_data = dotenv_values(".env")

    host = config_data["IP"]
    port = config_data["PORT"]
    username = config_data["USERNAME"]
    password = config_data["PASSWORD"]
    database = config_data["DATABASE"]

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"
#


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DATABASE_URL  # Get sqlalchemy url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
