import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from app.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash

client = TestClient(app)

def setup_test_user():
    db = SessionLocal()
    role = db.query(Role).filter(Role.name == "ADMIN").first()
    user = db.query(User).filter(User.username == "testwauser").first()
    if not user:
        user = User(
            username="testwauser", 
            email="testwauser@example.com", 
            hashed_password=get_password_hash("password123"), 
            role_id=role.id
        )
        db.add(user)
        db.commit()
    db.close()

def login():
    response = client.post("/api/v1/auth/login", data={"username": "testwauser", "password": "password123"})
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["data"]["access_token"]

def run_tests():
    setup_test_user()
    token = login()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Start Activity
    payload = {
        "category_id": 1,
        "activity_name": "Test Activity WA",
        "notes": "Testing WA module"
    }
    response = client.post("/api/v1/work-activities", json=payload, headers=headers)
    assert response.status_code == 201, f"Failed to start activity: {response.text}"
    activity_id = response.json()["data"]["id"]
    print("1. Start Activity - PASSED")
    
    # 2. Get Current Activity
    response = client.get("/api/v1/work-activities/current", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == activity_id
    print("2. Get Current Activity - PASSED")
    
    # 3. Start Another Activity (Should Fail)
    payload2 = {
        "category_id": 2,
        "activity_name": "Test Activity 2"
    }
    response = client.post("/api/v1/work-activities", json=payload2, headers=headers)
    assert response.status_code == 400, "Should have failed because user already has active activity"
    print("3. Negative Test: Start multiple active activities - PASSED")
    
    # 4. Finish Activity
    response = client.patch(f"/api/v1/work-activities/{activity_id}/finish", headers=headers)
    assert response.status_code == 200, f"Failed to finish activity: {response.text}"
    assert response.json()["data"]["status"] == "COMPLETED"
    print("4. Finish Activity - PASSED")
    
    # 5. Finish Activity Again (Should Fail)
    response = client.patch(f"/api/v1/work-activities/{activity_id}/finish", headers=headers)
    assert response.status_code == 400, "Should have failed because status is not WORKING"
    print("5. Negative Test: Finish non-WORKING activity - PASSED")
    
    print("All tests passed!")

if __name__ == '__main__':
    run_tests()
