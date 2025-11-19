import json
import pandas as pd
from datetime import datetime
import os

# ------------------------------
# Get environment variables
# ------------------------------
build_number = os.getenv("GITHUB_RUN_NUMBER", "0")
execution_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
repo = os.getenv("GITHUB_REPOSITORY")  # e.g., username/repo
repo_raw_url = f"https://raw.githubusercontent.com/{repo}/main/"

# ------------------------------
# Load raw JSON test results
# ------------------------------
with open("results/latest.json", "r") as f:
    data = json.load(f)

rows = []

for test in data.get("tests", []):
    nodeid = test.get("nodeid", "Unknown Test")
    outcome = test.get("outcome", "unknown")

    # Get duration and error
    call = test.get("call", {})
    duration = call.get("duration", 0)
    error = call.get("crash", {}).get("message", "")

    # Detect tests that likely did not run
    if duration == 0 and outcome == "passed" and not error:
        outcome = "did not run"
        error = "Test likely did not execute (environment issue)"

    # ------------------------------
    # Attach screenshot URL if exists
    # ------------------------------
    # Playwright plugin / conftest.py should write this
    screenshot_path = call.get("screenshot_path", "")
    if screenshot_path and os.path.exists(screenshot_path):
        screenshot_url = repo_raw_url + screenshot_path
    else:
        screenshot_url = ""

    # Append row
    rows.append({
        "build_number": int(build_number),
        "execution_time": execution_time,
        "name": nodeid,
        "status": outcome,
        "duration_ms": int(duration * 1000),
        "error": error,
        "screenshot": screenshot_url
    })

# ------------------------------
# Create DataFrame and save CSV
# ------------------------------
df = pd.DataFrame(rows)

# Save main processed CSV
os.makedirs("results", exist_ok=True)
csv_filename = "results/processed_results.csv"
df.to_csv(csv_filename, index=False, sep=",", encoding="utf-8-sig")

# Optionally, save per-run CSV for Option B
per_run_csv = f"results/history_{build_number}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(per_run_csv, index=False, sep=",", encoding="utf-8-sig")

print(df)
print(f"\nProcessed results saved to {csv_filename} and {per_run_csv}")
