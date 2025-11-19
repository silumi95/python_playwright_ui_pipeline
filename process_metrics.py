import json
import pandas as pd
from datetime import datetime
import os

# GitHub Actions environment variables
build_number = os.getenv("GITHUB_RUN_NUMBER", "0")
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

# Load JSON test results
with open("results/latest.json", "r") as f:
    data = json.load(f)

rows = []

for test in data.get("tests", []):
    nodeid = test.get("nodeid", "Unknown Test")
    outcome = test.get("outcome", "unknown")
    
    call = test.get("call", {})
    duration = call.get("duration", 0)
    error = call.get("crash", {}).get("message", "")
    
    # Detect likely not executed tests
    if duration == 0 and outcome == "passed" and not error:
        outcome = "did not run"
        error = "Test likely did not execute (environment issue)"
    
    rows.append({
        "build_number": int(build_number),
        "execution_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "name": nodeid,
        "status": outcome,
        "duration_ms": int(duration * 1000),
        "error": error
    })

df = pd.DataFrame(rows)

# Save CSV with build number and timestamp
csv_filename = f"history_{build_number}_{timestamp}.csv"
csv_path = f"results/{csv_filename}"
df.to_csv(csv_path, index=False, sep=",", encoding="utf-8-sig")

print(f"Processed results saved to {csv_path}")
