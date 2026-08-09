"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_db
from app.models import Base, User
from app.main import app
from app.auth.hashing import hash_password

engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture()
def test_user(db_session):
    user = User(
        user_login="tester1",
        name="Test User",
        hashed_password=hash_password("Test1234"),
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture()
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        json={"user_login": "tester1", "password": "Test1234"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.hashing import hash_password
from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base, Incident, User

# DATABASE_URL = "postgresql+psycopg://postgres:Test112234@localhost:5432/test"

engine = create_engine(settings.DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Create tables in ddbb whit the modesl.py structure


# client = TestClient(app)
@pytest.fixture
def client(db_session):
    # return TestClient(app)
    def override_get_db():
        try:
            yield db_session

        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db  # Session override

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture  # SQL Alchemy session
def db_session():

    db = TestingSessionLocal()

    # Clean database before every test
    db.query(Incident).delete()
    db.query(User).delete()
    db.commit()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture  # Create user for TESTS
def test_user(db_session):

    user = User(user_login="admin", name="Administrator", hashed_password=hash_password("admin123"), role="admin")

    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture  # Create token JWT
def auth_headers(client, test_user):

    response = client.post("/auth/login", json={"user_login": "admin", "password": "admin123"})

    token = response.json()["access_token"]

    # Returns formed authorization structure to use in tests as header for access incident endpoint
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture  # Gives valid incidence structure. This fixture gives a valid incident to be used in testT in test_incidents as base structure.
def valid_incident():
    return {
        "inc_title": "Cant Acces TS_bbdd_ux43",
        "inc_description": "Message said not valid user.",
        "inc_state": "assigned",
        "inc_priority": "high",
        "inc_assignee": "admin",
    }


@pytest.fixture  # Create valid incidence. This fixture creates a valid incident in bbdd to be used in tests in test_incidents as base incident.
def test_incident(db_session):

    incident = Incident(
        inc_title="Cant Acces TS_bbdd_ux43",
        inc_description="Message said not valid user.",
        inc_state="assigned",
        inc_priority="high",
        inc_assignee="admin",
    )

    db_session.add(incident)
    db_session.commit()
    db_session.refresh(incident)

    return incident
