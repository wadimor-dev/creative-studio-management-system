import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.user import User, RoleType
from app.auth.security import get_password_hash
from app.models.category import WorkCategory
from app.models.location import Location
from app.models.product_master import ProductMaster
from app.models.product import Product
from app.constants.product import ProductType
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wa08.db"

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
    # Setup test data
    db = TestingSessionLocal()
    
    # 1. Create User
    admin = User(username="testadmin", full_name="Test Admin", email="admin@test.com", password_hash=get_password_hash("password123"), role=RoleType.ADMIN)
    editor = User(username="testeditor", full_name="Test Editor", email="editor@test.com", password_hash=get_password_hash("password123"), role=RoleType.STAFF)
    db.add(admin)
    db.add(editor)
    
    # 2. Category
    cat = WorkCategory(name="Video Editing", expected_duration_hours=2)
    db.add(cat)
    
    # 3. Location
    loc = Location(name="Equipment Room", type="WAREHOUSE")
    db.add(loc)
    db.commit()
    
    # 4. Product Master & Product (Camera)
    pm = ProductMaster(sku_prefix="CAM", name="Camera Sony", description="Testing")
    db.add(pm)
    db.commit()
    
    prod = Product(
        sku="CAM-001",
        name="Camera Sony A7",
        display_name="Camera Sony A7",
        master_id=pm.id,
        type_id=ProductType.EQUIPMENT,
        category_id=cat.id,
        current_stock=10,
        location_id=loc.id
    )
    db.add(prod)
    db.commit()
    
    yield db
    
    # Teardown
    Base.metadata.drop_all(bind=engine)

def get_token(username="testeditor", password="password123"):
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_full_wa08_flow(db_session):
    token = get_token("testeditor", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create Activity
    cat_id = 1
    res = client.post("/work-activities/", json={
        "category_id": cat_id,
        "activity_name": "Edit Video Shopee",
        "notes": "Testing E2E"
    }, headers=headers)
    assert res.status_code == 201
    activity_id = res.json()["id"]
    
    # 2. Upload Before Evidence
    res = client.post(f"/work-activities/{activity_id}/evidence", data={"type": "BEFORE"}, files={"file": ("test.jpg", b"fakeimage", "image/jpeg")}, headers=headers)
    assert res.status_code == 200
    
    # 3. Borrow Asset
    # Mocking this for simplicity, usually this goes to /work-activities/{id}/assets
    res = client.post(f"/work-activities/{activity_id}/assets", json={
        "item_id": 1,
        "quantity": 1
    }, headers=headers)
    assert res.status_code == 200
    
    # 4. Start
    res = client.post(f"/work-activities/{activity_id}/start", headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "WORKING"
    
    # 5. Upload Progress
    res = client.post(f"/work-activities/{activity_id}/evidence", data={"type": "PROGRESS"}, files={"file": ("test2.jpg", b"fakeimage", "image/jpeg")}, headers=headers)
    assert res.status_code == 200
    
    # 6. Upload After
    res = client.post(f"/work-activities/{activity_id}/evidence", data={"type": "AFTER"}, files={"file": ("test3.jpg", b"fakeimage", "image/jpeg")}, headers=headers)
    assert res.status_code == 200
    
    # 7. Finish
    res = client.post(f"/work-activities/{activity_id}/finish", headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "COMPLETED"
    
    # 8. Check Dashboard
    admin_token = get_token("testadmin", "password123")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/dashboard", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["kpi"]["completed_tasks_today"] == 1
    
    # 9. Check Reports
    res = client.get("/reports?type=daily", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["total"] == 1
    
    # 10. Check Export limit & roles
    # Editor tries Export PDF (STAFF is allowed)
    res = client.post("/export/reports/pdf?type=daily", headers=headers)
    assert res.status_code == 200
    # Editor tries Export Excel (STAFF forbidden)
    res = client.post("/export/reports/excel?type=daily", headers=headers)
    assert res.status_code == 403
    
    # Admin tries Export Excel (Allowed)
    res = client.post("/export/reports/excel?type=daily", headers=admin_headers)
    assert res.status_code == 200

