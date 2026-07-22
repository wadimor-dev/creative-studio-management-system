import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database.base import Base
from app.core.database.session import get_db
from app.models.user import User, RoleType
from app.auth.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wa08_sec.db"

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
    admin = User(username="secadmin", email="sec@admin.com", password_hash=get_password_hash("pass"), role=RoleType.ADMIN)
    staff = User(username="secstaff", email="sec@staff.com", password_hash=get_password_hash("pass"), role=RoleType.STAFF)
    db.add(admin)
    db.add(staff)
    db.commit()
    yield db
    Base.metadata.drop_all(bind=engine)

def test_unauthorized_access(db_session):
    res = client.get("/dashboard")
    assert res.status_code == 401
    
    res = client.post("/export/reports/excel")
    assert res.status_code == 401

def test_forbidden_role_access(db_session):
    res = client.post("/auth/login", data={"username": "secstaff", "password": "pass"})
    token = res.json()["access_token"]
    
    # Staff cannot export excel
    res = client.post("/export/reports/excel?type=daily", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403

def test_file_upload_validation(db_session):
    res = client.post("/auth/login", data={"username": "secstaff", "password": "pass"})
    token = res.json()["access_token"]
    
    # Fake activity
    res_act = client.post("/work-activities/", json={"category_id": 1, "activity_name": "Test Sec"}, headers={"Authorization": f"Bearer {token}"})
    if res_act.status_code == 201:
        act_id = res_act.json()["id"]
        
        # Upload valid
        res_upload = client.post(f"/work-activities/{act_id}/evidence", data={"type": "BEFORE"}, files={"file": ("test.jpg", b"fake", "image/jpeg")}, headers={"Authorization": f"Bearer {token}"})
        assert res_upload.status_code == 200
        
        # Upload invalid extension
        res_upload = client.post(f"/work-activities/{act_id}/evidence", data={"type": "AFTER"}, files={"file": ("test.pdf", b"fake", "application/pdf")}, headers={"Authorization": f"Bearer {token}"})
        assert res_upload.status_code == 400

