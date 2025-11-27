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
        json={
            "user": "alice",
            "name": "Evening Ride",
            "calories": -320,
            "date": "2024-06-02",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Evening Ride"
    assert response.json()["user"] == "alice"

    other_user_activity = client.post(
        "/activities",
        json={
            "user": "bob",
            "name": "Swim",
            "calories": -150,
            "date": "2024-06-02",
        },
    )

    assert other_user_activity.status_code == 201

    activities = client.get("/activities", params={"user": "alice"})

    assert activities.status_code == 200
    body = activities.json()
    assert len(body) == 1
    assert body[0]["name"] == "Evening Ride"
    assert body[0]["calories"] == -320
    assert body[0]["user"] == "alice"


def test_log_food_and_list(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)
    client = TestClient(app)

    response = client.post(
        "/foods",
        json={
            "user": "alice",
            "name": "Oatmeal",
            "calories": 150,
            "date": "2024-06-03",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Oatmeal"
    assert response.json()["user"] == "alice"

    other_user_food = client.post(
        "/foods",
        json={
            "user": "bob",
            "name": "Toast",
            "calories": 90,
            "date": "2024-06-03",
        },
    )

    assert other_user_food.status_code == 201

    foods = client.get("/foods", params={"user": "alice"})

    assert foods.status_code == 200
    body = foods.json()
    assert len(body) == 1
    assert body[0]["name"] == "Oatmeal"
    assert body[0]["calories"] == 150
    assert body[0]["user"] == "alice"


def test_list_logs(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)
    client = TestClient(app)

    client.post(
        "/foods",
        json={"user": "alice", "name": "Toast", "calories": 120, "date": "2024-06-04"},
    )
    client.post(
        "/activities",
        json={"user": "alice", "name": "Swim", "calories": -400, "date": "2024-06-04"},
    )
    client.post(
        "/foods",
        json={"user": "bob", "name": "Cereal", "calories": 200, "date": "2024-06-04"},
    )

    logs = client.get("/logs", params={"user": "alice"})

    assert logs.status_code == 200
    body = logs.json()
    assert len(body) == 2
    assert body[0]["name"] == "Toast"
    assert body[1]["name"] == "Swim"
    assert all(entry["user"] == "alice" for entry in body)


def test_daily_summary(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)
    client = TestClient(app)

    client.post(
        "/activities",
        json={
            "user": "alice",
            "name": "Morning Run",
            "calories": -350,
            "date": "2024-06-01",
        },
    )
    db.insert_event("alice", "Lunch", 650, "2024-06-01")
    db.insert_event("bob", "Coffee", 5, "2024-06-02")

    summary = client.get("/summary", params={"user": "alice", "date": "2024-06-01"})

    assert summary.status_code == 200
    payload = summary.json()
    assert payload["date"] == "2024-06-01"
    assert payload["user"] == "alice"
    assert payload["total_food"] == 650
    assert payload["total_activities"] == 350
    assert payload["net_calories"] == 300
