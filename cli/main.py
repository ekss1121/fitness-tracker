from datetime import date
import sys
from typing import Iterable

import click

from events import Event, get_events, log_event


def _supports_emoji() -> bool:
    encoding = (sys.stdout.encoding or "utf-8").lower()
    return "utf" in encoding


def _emoji(icon: str, fallback: str) -> str:
    return icon if _supports_emoji() else fallback


def _format_summary(events: Iterable[Event]) -> str:
    total_food = sum(event.calories for event in events if event.calories > 0)
    total_activities = sum(-event.calories for event in events if event.calories < 0)
    net_calories = total_food - total_activities
    rows = [
        (_emoji("🥗 Food", "Food"), total_food),
        (_emoji("🏃 Activities", "Activities"), total_activities),
        (_emoji("⚖️ Net", "Net"), net_calories),
    ]
    label_width = max(len(label) for label, _ in rows)
    return "\n".join(
        f"{label:<{label_width}}  {value:>7.1f} calories" for label, value in rows
    )


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Fitness tracker CLI."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(show)


@cli.command()
@click.option("--user", required=False, default="default", help="User identifier for the log.")
def show(user: str) -> None:
    """Display totals for logged events."""
    events = get_events(user=user)
    if not events:
        click.secho("No events logged yet. Log food or activities to see a summary.", fg="yellow")
        return
    click.secho(_emoji("📊 Daily Summary", "Daily Summary"), fg="cyan", bold=True)
    click.echo(_format_summary(events))


@cli.command()
@click.argument("name")
@click.argument("calories", type=float)
@click.option(
    "--date",
    "event_date",
    help="ISO date (YYYY-MM-DD); defaults to today.",
)
@click.option("--user", required=False, default="default", help="User identifier for the log.")
def log(name: str, calories: float, event_date: str | None, user: str) -> None:
    """Log a food (positive) or activity (negative) entry."""
    resolved_date = event_date or date.today().isoformat()
    log_event(Event(user=user, name=name, calories=calories, date=resolved_date))
    emoji = _emoji("🍎", "OK") if calories > 0 else _emoji("🔥", "OK")
    click.secho(
        f"{emoji} Logged '{name}' ({calories} cal) for user '{user}' on {resolved_date}.",
        fg="green",
    )


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
