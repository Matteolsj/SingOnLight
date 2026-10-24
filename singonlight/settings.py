"""Paths and settings shared by the application modules."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "singonlight.db"
SIMULATION_MODE = os.getenv("SINGONLIGHT_SIMULATION", "0").lower() in {
    "1", "true", "yes", "on"
}