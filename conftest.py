import os
import time
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
# yield to let pytest run other hooks and get the test report
 outcome = yield
 report = outcome.get_result()


# Capture screenshot on any failure (setup, call, teardown)
 if report.failed:
    page = item.funcargs.get("page", None)
    print(f"[DEBUG] Test {item.nodeid} failed during {report.when}, page={page}")

    if page:
        screenshots_dir = os.path.abspath("results/screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        filename = (
            f"{int(time.time())}_"
            + item.nodeid.replace("/", "_")
                         .replace("::", "_")
                         .replace(" ", "_")
            + ".png"
        )
        screenshot_path = os.path.join(screenshots_dir, filename)

        try:
            page.screenshot(path=screenshot_path)
            print(f"[DEBUG] Screenshot saved: {screenshot_path}")
            report.screenshot_path = screenshot_path
            call.screenshot_path = screenshot_path
        except Exception as e:
            print(f"[ERROR] Failed to take screenshot: {e}")

