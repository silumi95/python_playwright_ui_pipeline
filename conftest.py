import os
import time
import json
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Extract metadata from marker
    metadata_marker = item.get_closest_marker("metadata")
    metadata = {}
    if metadata_marker:
        metadata = {
            "severity": metadata_marker.kwargs.get("severity", ""),
            "priority": metadata_marker.kwargs.get("priority", ""),
            "executed_by": metadata_marker.kwargs.get("executed_by", ""),
            "defect": metadata_marker.kwargs.get("defect", "")
        }

    # Append metadata into longrepr so it is written into JSON
    if report.when == "call":
        meta_str = json.dumps(metadata)
        if report.longrepr:
            report.longrepr = f"{report.longrepr}\nMETADATA:{meta_str}"
        else:
            report.longrepr = f"METADATA:{meta_str}"

        # Save screenshot on failure
        if report.failed:
            page = item.funcargs.get("page")
            if page:
                screenshots_dir = os.path.abspath("results/screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)
                safe_name = item.nodeid.replace("/", "_").replace("::", "_").replace("[", "_").replace("]", "_").replace(" ", "_")
                filename = f"{int(time.time())}_{safe_name}.png"
                screenshot_path = os.path.join(screenshots_dir, filename)
                page.screenshot(path=screenshot_path)
                report.longrepr += f"\nSCREENSHOT:{screenshot_path}"
