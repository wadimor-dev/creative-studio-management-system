import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.user import User, RoleType
from app.auth.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wa08_perf.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    admin = User(username="perfadmin", email="perf@admin.com", password_hash=get_password_hash("pass"), role=RoleType.ADMIN)
    db.add(admin)
    db.commit()
    yield db
    Base.metadata.drop_all(bind=engine)

def test_benchmark_login(db_session):
    start = time.time()
    res = client.post("/auth/login", data={"username": "perfadmin", "password": "pass"})
    duration = time.time() - start
    
    assert res.status_code == 200
    assert duration < 0.850 # Target < 850ms

def test_benchmark_dashboard(db_session):
    res = client.post("/auth/login", data={"username": "perfadmin", "password": "pass"})
    token = res.json()["access_token"]
    
    start = time.time()
    res2 = client.get("/dashboard", headers={"Authorization": f"Bearer {token}"})
    duration = time.time() - start
    
    assert res2.status_code == 200
    assert duration < 1.400 # Target < 1.4s

def test_benchmark_reports(db_session):
    res = client.post("/auth/login", data={"username": "perfadmin", "password": "pass"})
    token = res.json()["access_token"]
    
    start = time.time()
    res2 = client.get("/reports?type=daily", headers={"Authorization": f"Bearer {token}"})
    duration = time.time() - start
    
    assert res2.status_code == 200
    assert duration < 3.000 # Target < 3s

