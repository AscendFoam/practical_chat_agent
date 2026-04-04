from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from practical_chat_agent.app.config import Settings


def create_engine_from_settings(settings: Settings) -> Engine:
    return create_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.mysql_echo,
        pool_pre_ping=True,
        future=True,
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def create_database_if_missing(settings: Settings) -> None:
    database_name = settings.validated_database_name()
    server_engine = create_engine(
        settings.sqlalchemy_server_uri,
        echo=settings.mysql_echo,
        pool_pre_ping=True,
        future=True,
    )
    with server_engine.connect() as connection:
        connection.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
            ),
        )
        connection.commit()

