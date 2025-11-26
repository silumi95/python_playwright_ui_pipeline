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

# GitHub repository info
GITHUB_USER = "silumi95"
GITHUB_REPO = "python_playwright_ui_pipeline"
GITHUB_BRANCH = "main"
repo_url_base = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/results/screenshots/"

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
# Helper: Extract metadata safely
# -----------------------------

def extract_metadata(test):
    """Extract metadata from longrepr JSON string"""
    longrepr = test.get("call", {}).get("longrepr", "")
    if "METADATA:" in longrepr:
        try:
            meta_str = longrepr.split("METADATA:")[1].split("\n")[0]
            return json.loads(meta_str)
        except:
            return {}
    return {}


# -----------------------------
# Parse test results
# -----------------------------
rows = []

for test in tests:
    nodeid = test.get("nodeid", "Unknown Test")
    outcome = test.get("outcome", "unknown")
    call = test.get("call", {})
    duration = call.get("duration", 0)
    duration_ms = int(duration * 1000)

    # Extract error
    error = ""
    if call.get("crash"):
        error = call["crash"].get("message", "")
    elif test.get("excinfo"):
        error = str(test.get("excinfo", ""))

    # Detect likely not-run tests
    if duration == 0 and outcome == "passed" and not error:
        outcome = "did not run"
        error = "Test likely did not execute (environment issue)"

    # Screenshot → GitHub URL
    screenshot_url = ""
    longrepr = call.get("longrepr", "")
    if longrepr and "SCREENSHOT:" in longrepr:
        screenshot_path = longrepr.split("SCREENSHOT:")[1].strip()
        screenshot_filename = os.path.basename(screenshot_path)
        screenshot_url = repo_url_base + screenshot_filename

    # Metadata
    metadata = extract_metadata(test)
    severity = metadata.get("severity", "")
    priority = metadata.get("priority", "")
    executed_by = metadata.get("executed_by", "")
    defect = metadata.get("defect", "")

    rows.append({
        "build_number": int(build_number),
        "execution_time": execution_time,
        "name": nodeid,
        "status": outcome,
        "duration_ms": duration_ms,
        "severity": severity,
        "priority": priority,
        "executed_by": executed_by,
        "defect": defect,
        "error": error,
        "longrepr": longrepr,
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
