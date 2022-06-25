import pytest
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from dhp.models._base import engine


@pytest.fixture(scope="session")
def connection():
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    # NOOP, we don't yet have data to seed, yet.
    ...


@pytest.fixture
def db_session(setup_database, connection) -> Session:
    transaction = connection.begin()

    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )

    transaction.rollback()
