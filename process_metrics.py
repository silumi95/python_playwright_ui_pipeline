import json
import pandas as pd

# Load raw JSON
with open("results/latest.json", "r") as f:
    data = json.load(f)

rows = []

for test in data.get("tests", []):
    nodeid = test.get("nodeid", "Unknown Test")
    outcome = test.get("outcome", "unknown")
    
    # If test has call info, get duration and error
    call = test.get("call", {})
    duration = call.get("duration", 0)
    error = ""
    if "crash" in call:
        error = call["crash"].get("message", "")
    
    # Detect tests that likely didn't run
    if duration == 0 and outcome == "passed" and not error:
        outcome = "did not run"
        error = "Test likely did not execute (network/browser issue)"

    rows.append({
        "name": nodeid,
        "status": outcome,
        "duration_ms": int(duration * 1000),  # convert seconds to ms
        "error": error
    })

df = pd.DataFrame(rows)
df.to_csv("results/processed_results.csv", index=False)
print(df)
print("\nProcessed results saved to results/processed_results.csv")
