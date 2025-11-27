from datetime import date
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from events import Event, get_events, log_event


class Activity(BaseModel):
    user: str
    name: str
    calories: float
    date: str


class Food(BaseModel):
    user: str
    name: str
    calories: float
    date: str


class LogEventRequest(BaseModel):
    user: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    calories: float
    date: str | None = None


class LogEntry(BaseModel):
    user: str
    name: str
    calories: float
    date: str


class DailySummary(BaseModel):
    user: str
    date: str
    total_food: float
    total_activities: float
    net_calories: float


def _normalize_date(value: str | None) -> str:
    return value or date.today().isoformat()


def _build_event(event: LogEventRequest) -> Event:
    """Create an Event from request data with a normalized date."""
    resolved_date = _normalize_date(event.date)
    return Event(user=event.user, name=event.name, calories=event.calories, date=resolved_date)


def _summarize_day(events: List[Event], summary_date: str, user: str) -> DailySummary:
    relevant_events = [event for event in events if event.date == summary_date and event.user == user]
    total_food = sum(event.calories for event in relevant_events if event.calories > 0)
    total_activities = sum(-event.calories for event in relevant_events if event.calories < 0)
    net_calories = total_food - total_activities
    return DailySummary(
        user=user,
        date=summary_date,
        total_food=total_food,
        total_activities=total_activities,
        net_calories=net_calories,
    )


app = FastAPI(title="Fitness Tracker API")


@app.get("/activities", response_model=List[Activity])
def list_activities(user: str) -> List[Activity]:
    events = get_events(user=user)
    return [
        Activity(user=event.user, name=event.name, calories=event.calories, date=event.date)
        for event in events
        if event.calories < 0
    ]


@app.get("/foods", response_model=List[Food])
def list_foods(user: str) -> List[Food]:
    events = get_events(user=user)
    return [
        Food(
            user=event.user,
            name=event.name,
            calories=event.calories,
            date=event.date,
        )
        for event in events
        if event.calories > 0
    ]


@app.get("/logs", response_model=List[LogEntry])
def list_logs(user: str) -> List[LogEntry]:
    events = get_events(user=user)
    return [
        LogEntry(user=event.user, name=event.name, calories=event.calories, date=event.date)
        for event in events
    ]


@app.get("/summary", response_model=DailySummary)
def get_daily_summary(user: str, date: str | None = None) -> DailySummary:
    summary_date = _normalize_date(date)
    events = get_events(user=user)
    return _summarize_day(events, summary_date, user)


@app.post("/activities", response_model=Activity, status_code=201)
def log_activity(event: LogEventRequest) -> Activity:
    activity = _build_event(event)
    log_event(activity)
    return Activity(
        user=activity.user,
        name=activity.name,
        calories=activity.calories,
        date=activity.date,
    )


@app.post("/foods", response_model=Food, status_code=201)
def log_food(event: LogEventRequest) -> Food:
    food = _build_event(event)
    log_event(food)
    return Food(
        user=food.user,
        name=food.name,
        calories=food.calories,
        date=food.date,
    )
