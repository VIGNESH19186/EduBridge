"""
One-shot setup helper: copies .env.example to .env (if missing) and reminds
the user of next steps. Does not install packages (use pip directly).
"""
import os
import shutil

ROOT = os.path.join(os.path.dirname(__file__), "..")


def main():
    env_path = os.path.join(ROOT, ".env")
    example_path = os.path.join(ROOT, ".env.example")

    if not os.path.exists(env_path):
        shutil.copyfile(example_path, env_path)
        print("Created .env from .env.example. Edit it to add your AI_API_KEY (optional).")
    else:
        print(".env already exists, leaving it untouched.")

    print("\nNext steps:")
    print("  1. pip install -r requirements.txt")
    print("  2. python scripts/seed_database.py")
    print("  3. uvicorn backend.main:app --reload")
    print("  4. Open http://localhost:8000 in your browser")


if __name__ == "__main__":
    main()
