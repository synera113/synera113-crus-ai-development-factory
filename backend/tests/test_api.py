import os

os.environ["CRUS_DATABASE_URL"] = "sqlite:///./test-phase1.db"
os.environ["CRUS_MODE"] = "demo"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ten_demo_agents():
    response = client.get("/api/agents")
    assert response.status_code == 200
    assert len(response.json()) == 10
    assert all(agent["demo"] is True for agent in response.json())


def test_project_and_task_crud():
    response = client.post("/api/projects", json={
        "name": "Test Projesi",
        "description": "Phase 1 API test projesi",
        "project_type": "web_application",
        "priority": "HIGH",
    })
    assert response.status_code == 201
    project = response.json()

    response = client.post(f"/api/projects/{project['id']}/tasks", json={
        "title": "API tasarımı",
        "description": "REST uçlarını tasarla",
        "priority": "HIGH",
        "agent_role": "ARCHITECT",
    })
    assert response.status_code == 201

    response = client.get("/api/projects")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_dashboard():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    assert response.json()["mode"] == "demo"
