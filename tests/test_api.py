import db
from fastapi.testclient import TestClient

from api import app


def _use_temp_db(monkeypatch, tmp_path):
    test_db = tmp_path / "test_api.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)
    return test_db


def test_log_activity_and_list(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)
    client = TestClient(app)

    response = client.post(
        "/activities",
        json={"name": "Evening Ride", "calories": -320, "date": "2024-06-02"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Evening Ride"

    activities = client.get("/activities")

    assert activities.status_code == 200
    body = activities.json()
    assert len(body) == 1
    assert body[0]["name"] == "Evening Ride"
    assert body[0]["calories"] == -320


def test_daily_summary(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)
    client = TestClient(app)

    client.post(
        "/activities",
        json={"name": "Morning Run", "calories": -350, "date": "2024-06-01"},
    )
    db.insert_event("Lunch", 650, "2024-06-01")
    db.insert_event("Coffee", 5, "2024-06-02")

    summary = client.get("/summary", params={"date": "2024-06-01"})

    assert summary.status_code == 200
    payload = summary.json()
    assert payload["date"] == "2024-06-01"
    assert payload["total_food"] == 650
    assert payload["total_activities"] == 350
    assert payload["net_calories"] == 300
