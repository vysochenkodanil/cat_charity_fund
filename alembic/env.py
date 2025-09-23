from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.core.db import Base  # импортируем Base с метаданными
import app.models.charity_project  # чтобы подхватились модели
import app.models.donation
import app.models.user


config = context.config
fileConfig(config.config_file_name)

# Используем синхронный драйвер SQLite
config.set_main_option("sqlalchemy.url", settings.database_url.replace("+aiosqlite", ""))

target_metadata = Base.metadata


def run_migrations_offline():
    """Миграции в offline-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Миграции в online-режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
