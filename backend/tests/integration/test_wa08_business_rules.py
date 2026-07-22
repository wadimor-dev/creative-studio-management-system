import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database.base import Base
from app.core.database.session import get_db
from app.models.user import User, RoleType
from app.auth.security import get_password_hash
from app.models.category import WorkCategory

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wa08_rules.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
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
    editor = User(username="testeditor2", full_name="Test Editor", email="editor2@test.com", password_hash=get_password_hash("password123"), role=RoleType.STAFF)
    db.add(editor)
    cat = WorkCategory(name="Video Editing", expected_duration_hours=2)
    db.add(cat)
    db.commit()
    yield db
    Base.metadata.drop_all(bind=engine)

def get_token():
    res = client.post("/auth/login", data={"username": "testeditor2", "password": "password123"})
    return res.json()["access_token"]

def test_start_without_before_fails(db_session):
    headers = {"Authorization": f"Bearer {get_token()}"}
    res = client.post("/work-activities/", json={"category_id": 1, "activity_name": "Test Rules"}, headers=headers)
    assert res.status_code == 201
    act_id = res.json()["id"]
    
    # Try start
    res2 = client.post(f"/work-activities/{act_id}/start", headers=headers)
    assert res2.status_code == 400
    assert "Evidence BEFORE is missing" in res2.json()["detail"] or "must upload BEFORE" in res2.json()["detail"] or "Tidak bisa memulai" in res2.json()["detail"]

def test_finish_without_after_fails(db_session):
    headers = {"Authorization": f"Bearer {get_token()}"}
    res = client.post("/work-activities/", json={"category_id": 1, "activity_name": "Test Rules 2"}, headers=headers)
    act_id = res.json()["id"]
    
    # Upload Before
    client.post(f"/work-activities/{act_id}/evidence", data={"type": "BEFORE"}, files={"file": ("t.jpg", b"x", "image/jpeg")}, headers=headers)
    # Start
    client.post(f"/work-activities/{act_id}/start", headers=headers)
    
    # Try finish
    res2 = client.post(f"/work-activities/{act_id}/finish", headers=headers)
    assert res2.status_code == 400
    assert "Evidence AFTER is missing" in res2.json()["detail"] or "must upload AFTER" in res2.json()["detail"] or "Tidak bisa menyelesaikan" in res2.json()["detail"]
