import os
import sys
import pytest

# -----------------------------------------------------------
# 1. Ensure project root is in PYTHONPATH (your request)
# -----------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# -----------------------------------------------------------
# 2. Pytest hook to capture screenshots when a test fails
# -----------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Run the actual test first
    outcome = yield
    report = outcome.get_result()

    # Capture ONLY for failed tests and only at the "call" stage (after execution)
    if report.when == "call" and report.failed:

        # Get Playwright "page" fixture (only exists for UI tests)
        page = item.funcargs.get("page", None)

        if page:
            # Ensure screenshot folder exists
            os.makedirs("results/screenshots", exist_ok=True)

            # Generate a safe file name
            filename = (
                item.nodeid
                .replace("/", "_")
                .replace("::", "_")
                .replace(" ", "_")
                + ".png"
            )

            screenshot_path = f"results/screenshots/{filename}"

            # Take screenshot
            page.screenshot(path=screenshot_path)

            # Store path so process_metrics.py can pick it up
            report.screenshot_path = screenshot_path

            # Attach screenshot path to pytest result object (JSON plugin will include it)
            if hasattr(call, "result"):
                call.result = screenshot_path
