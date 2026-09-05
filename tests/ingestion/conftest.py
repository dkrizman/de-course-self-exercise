import pytest
import psycopg

from alembic import command
from alembic.config import Config
from testcontainers.community.postgres import PostgresContainer


@pytest.fixture(scope="function")
def connection():

    with PostgresContainer("postgres:16") as postgres:

        database_url = postgres.get_connection_url(driver="psycopg")

        alembic_config = Config("alembic.ini")
        alembic_config.set_main_option("sqlalchemy.url", database_url)
        command.upgrade(alembic_config, "head")

        alembic_config.set_main_option(
            "sqlalchemy.url",
            database_url,
        )

        command.upgrade(
            alembic_config,
            "head",
        )

        connection = psycopg.connect(database_url.replace("postgresql+psycopg://", "postgresql://"))
        yield connection

        connection.close()