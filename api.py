from datetime import date
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from events import Event, get_events, log_event


class Activity(BaseModel):
    name: str
    calories: float
    date: str


class LogEventRequest(BaseModel):
    name: str = Field(..., min_length=1)
    calories: float
    date: str | None = None


class DailySummary(BaseModel):
    date: str
    total_food: float
    total_activities: float
    net_calories: float


def _normalize_date(value: str | None) -> str:
    return value or date.today().isoformat()


def _summarize_day(events: List[Event], summary_date: str) -> DailySummary:
    relevant_events = [event for event in events if event.date == summary_date]
    total_food = sum(event.calories for event in relevant_events if event.calories > 0)
    total_activities = sum(-event.calories for event in relevant_events if event.calories < 0)
    net_calories = total_food - total_activities
    return DailySummary(
        date=summary_date,
        total_food=total_food,
        total_activities=total_activities,
        net_calories=net_calories,
    )


app = FastAPI(title="Fitness Tracker API")


@app.get("/activities", response_model=List[Activity])
def list_activities() -> List[Activity]:
    events = get_events()
    return [
        Activity(name=event.name, calories=event.calories, date=event.date)
        for event in events
        if event.calories < 0
    ]


@app.get("/summary", response_model=DailySummary)
def get_daily_summary(date: str | None = None) -> DailySummary:
    summary_date = _normalize_date(date)
    events = get_events()
    return _summarize_day(events, summary_date)


@app.post("/activities", response_model=Activity, status_code=201)
def log_activity(event: LogEventRequest) -> Activity:
    event_date = _normalize_date(event.date)
    activity = Event(name=event.name, calories=event.calories, date=event_date)
    log_event(activity)
    return Activity(name=activity.name, calories=activity.calories, date=activity.date)
