"""
Convenience wrapper so seeding can be run from the project root:
    python scripts/seed_database.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.database.seed import seed  # noqa: E402

if __name__ == "__main__":
    seed()
