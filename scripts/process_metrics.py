import json
import pandas as pd
from datetime import datetime
import os

# -----------------------------
# Config
# -----------------------------
results_dir = "results"
screenshots_dir = os.path.join(results_dir, "screenshots")
latest_json_file = os.path.join(results_dir, "latest.json")
build_number = os.getenv("GITHUB_RUN_NUMBER", "0")
execution_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# GitHub repository info (update these)
GITHUB_USER = "YOUR_USERNAME"
GITHUB_REPO = "YOUR_REPO_NAME"
GITHUB_BRANCH = "main"  # or your branch
repo_url_base = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/results/screenshots/"

# Ensure directories exist
os.makedirs(results_dir, exist_ok=True)
os.makedirs(screenshots_dir, exist_ok=True)

# -----------------------------
# Load JSON
# -----------------------------
if not os.path.exists(latest_json_file):
    print(f"❌ File not found: {latest_json_file}")
    exit(1)

with open(latest_json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

tests = data.get("tests", [])
print(f"Found {len(tests)} tests in JSON")

if not tests:
    print("❌ No test data found in JSON")
    exit(1)

# -----------------------------
# Parse test results
# -----------------------------
rows = []

for test in tests:
    nodeid = test.get("nodeid", "Unknown Test")
    outcome = test.get("outcome", "unknown")
    duration = test.get("call", {}).get("duration", 0)
    duration_ms = int(duration * 1000)

    # Extract error message
    error = ""
    call = test.get("call", {})
    if call.get("crash"):
        error = call["crash"].get("message", "")
    elif test.get("excinfo"):
        error = str(test.get("excinfo", ""))

    # Detect tests that likely did not run
    if duration == 0 and outcome == "passed" and not error:
        outcome = "did not run"
        error = "Test likely did not execute (environment issue)"

    # Screenshot path → GitHub raw URL
    screenshot_path = call.get("screenshot_path", "")
    if screenshot_path and os.path.exists(screenshot_path):
        screenshot_filename = os.path.basename(screenshot_path)
        screenshot_url = repo_url_base + screenshot_filename
    else:
        screenshot_url = ""

    rows.append({
        "build_number": int(build_number),
        "execution_time": execution_time,
        "name": nodeid,
        "status": outcome,
        "duration_ms": duration_ms,
        "error": error,
        "screenshot": screenshot_url
    })

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(rows)
print(df)

# -----------------------------
# Save per-run CSV
# -----------------------------
processed_csv = os.path.join(results_dir, f"processed_results_{build_number}.csv")
df.to_csv(processed_csv, index=False, encoding="utf-8-sig")
print(f"✅ Processed CSV saved at {processed_csv}")

# -----------------------------
# Append to history.csv
# -----------------------------
history_csv = os.path.join(results_dir, "history.csv")
if os.path.exists(history_csv):
    df_existing = pd.read_csv(history_csv)
    df = pd.concat([df_existing, df], ignore_index=True)

df.to_csv(history_csv, index=False, encoding="utf-8-sig")
print(f"✅ History CSV updated at {history_csv}")
