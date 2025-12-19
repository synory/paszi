from fastapi.testclient import TestClient
from app.main import app
from fastapi.testclient import TestClient
from app.main import app
from app.db import SessionLocal
from app.models import User
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_users():
    db = SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

def test_register_success():
    resp = client.post("/api/register", json={
        "login": "testuser",
        "password": "Str0ngP@ss1",
    })
    assert resp.status_code == 200
    assert resp.json()["message"] == "user создан"

def test_duplicate_login():
    client.post("/api/register", json={
        "login": "user",
        "password": "Str0ngP@ss1",
    })
    resp = client.post("/api/register", json={
        "login": "user",
        "password": "Str0ngP@ss1",
    })
    assert resp.status_code == 409

def test_weak_password():
    resp = client.post("/api/register", json={
        "login": "weak",
        "password": "weak",
    })
    assert resp.status_code == 422
