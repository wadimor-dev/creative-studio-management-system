import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database.base import Base
from app.core.database.session import get_db
from app.core.config import settings
from app.models.user import User
from app.models.role import Role
from app.constants.role import RoleType
from app.main import app

# Create in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Create default roles
    admin_role = Role(id=1, name=RoleType.ADMIN)
    staff_role = Role(id=2, name=RoleType.STAFF)
    session.add_all([admin_role, staff_role])
    session.commit()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_user(db):
    from app.core.authorization.repositories import user_role_repo
    user = User(
        username="admin_test",
        email="admin@test.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_role_repo.set_user_roles(db, user.id, [1])
    return user

@pytest.fixture(scope="function")
def auth_client(client, admin_user):
    from app.core.database.session import SessionLocal
    from app.core.auth.session import session_service as svc
    db = SessionLocal()
    try:
        _, access_token, _ = svc.create_session(
            db=db,
            user_id=admin_user.id,
        )
    finally:
        db.close()

    token = access_token
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
