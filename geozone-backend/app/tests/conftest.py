import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.dependecies import get_db
from app.main import app
from app.middleware.dependencies import get_current_user
from app.middleware.jwt import create_access_token
from app.modules.auth.infrastructure.models.auth_credentials import Auth_Credentials
from app.modules.auth.service.auth_service import AuthService
from app.modules.models.base import Base

TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

engine = create_engine(TEST_DATABASE_URL,)
TestingSessionLocal = sessionmaker( autocommit=False, autoflush=False,expire_on_commit=False,bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """ Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """
    Test Client with test database injected
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create_test_user(db_session) -> Auth_Credentials:
    """ Insert a test user into the test database"""

    user = Auth_Credentials(
        email="test@example.com",
        hashpassword=AuthService._get_password("fakehash"),
        role="user",
        email_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture(scope="function")
def authenticated_client(db_session):
    """ TestClient with both test DB and a fake authenticated user"""
    test_user = create_test_user(db_session)
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def ovverride_get_current_user():
        return test_user
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = ovverride_get_current_user

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def normal_user_token():
    """
    Create a token for normal user 
    """

    return create_access_token(
        subject="12345",
        role="user",
        email_verified=False,
        expires_delta=15
        )