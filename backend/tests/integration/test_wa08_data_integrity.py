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
from app.models.product_master import ProductMaster
from app.models.product import Product
from app.constants.product import ProductType
from app.models.inventory_transaction import InventoryTransaction

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wa08_integrity.db"
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
    editor = User(username="testeditor3", email="editor3@test.com", password_hash=get_password_hash("pass"), role=RoleType.STAFF)
    db.add(editor)
    cat = WorkCategory(name="Editing", expected_duration_hours=2)
    db.add(cat)
    pm = ProductMaster(sku_prefix="ITM", name="Item")
    db.add(pm)
    db.commit()
    prod = Product(sku="ITM-01", name="Item 1", current_stock=10, master_id=pm.id, type_id=ProductType.EQUIPMENT, category_id=cat.id)
    db.add(prod)
    db.commit()
    yield db
    Base.metadata.drop_all(bind=engine)

def test_stock_integrity_on_borrow_and_return(db_session):
    res_login = client.post("/auth/login", data={"username": "testeditor3", "password": "pass"})
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create activity
    res_act = client.post("/work-activities/", json={"category_id": 1, "activity_name": "Integrity Test"}, headers=headers)
    act_id = res_act.json()["id"]
    
    # 2. Check initial stock is 10
    prod = db_session.query(Product).first()
    assert prod.current_stock == 10
    
    # 3. Upload Before & Start
    client.post(f"/work-activities/{act_id}/evidence", data={"type": "BEFORE"}, files={"file": ("t.jpg", b"x", "image/jpeg")}, headers=headers)
    client.post(f"/work-activities/{act_id}/start", headers=headers)
    
    # 4. Borrow Asset (we assume borrowing creates OUT transaction and reduces stock)
    client.post(f"/work-activities/{act_id}/assets", json={"item_id": 1, "quantity": 2}, headers=headers)
    
    # Stock should be 8
    db_session.refresh(prod)
    assert prod.current_stock == 8
    
    # Check transaction OUT
    tx_out = db_session.query(InventoryTransaction).filter_by(item_id=1, quantity=2).first()
    assert tx_out is not None
    assert tx_out.type.value == "OUT"
    
    # 5. Upload After & Finish
    client.post(f"/work-activities/{act_id}/evidence", data={"type": "AFTER"}, files={"file": ("t.jpg", b"x", "image/jpeg")}, headers=headers)
    client.post(f"/work-activities/{act_id}/finish", headers=headers)
    
    # 6. Auto Return should happen, stock back to 10
    db_session.refresh(prod)
    assert prod.current_stock == 10
    
    # Check transaction IN (RETURN)
    tx_in = db_session.query(InventoryTransaction).filter_by(item_id=1, quantity=2).order_by(InventoryTransaction.id.desc()).first()
    assert tx_in is not None
    assert tx_in.type.value == "RETURN" or tx_in.type.value == "IN"
