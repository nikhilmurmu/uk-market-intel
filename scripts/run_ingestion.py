import sys
sys.path.insert(0, "app")
from ingestion.scheduler import run_all

if __name__ == "__main__":
    data = run_all()
    if not data:
        sys.exit(1)
    print("Ingestion successful.")
