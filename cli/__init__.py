"""Command-line interface for the fitness tracker."""

from pathlib import Path
import sys

# Ensure project root is on sys.path so imports like `events` work when invoked via the console script.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from .main import main

__all__ = ["main"]
