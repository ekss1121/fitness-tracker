from typing import List

from events import Event, get_events


def main() -> None:
    events: List[Event] = get_events(user="default")

    total_food = sum(event.calories for event in events if event.calories > 0)
    total_activities = sum(-event.calories for event in events if event.calories < 0)

    net_calories = total_food - total_activities
    rows = [
        ("Total Food ?? :", total_food),
        ("Total Activities ??? :", total_activities),
        ("Net Calories ?? :", net_calories),
    ]
    label_width = max(len(label) for label, _ in rows)
    for label, value in rows:
        print(f"{label:<{label_width}}  {value:>4} calories")


def log_sample_events() -> None:
    """Example helper to log sample events when experimenting locally."""
    from events import log_event

    eat_apple = Event(user="default", name="Apple", calories=95)
    log_event(eat_apple)
    run_5k = Event(user="default", name="Running 5K", calories=-300)
    log_event(run_5k)


if __name__ == "__main__":
    main()
