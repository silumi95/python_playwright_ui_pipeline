import os
import time
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            screenshots_dir = os.path.abspath("results/screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            safe_name = (
                item.nodeid
                .replace("/", "_")
                .replace("::", "_")
                .replace(" ", "_")
                .replace("[", "_")
                .replace("]", "_")
            )

            filename = f"{int(time.time())}_{safe_name}.png"
            screenshot_path = os.path.join(screenshots_dir, filename)

            page.screenshot(path=screenshot_path)
            print(f"[DEBUG] Screenshot saved: {screenshot_path}")

            # WORKS ON ALL ORIGINAL VERSIONS OF PYTEST-JSON-REPORT
            report.longrepr = f"{report.longrepr}\nSCREENSHOT:{screenshot_path}"
