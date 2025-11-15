import os
from datetime import datetime

# Create timestamped result directories
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RESULT_DIR = os.path.join("results", f"run_{timestamp}")
SCREENSHOT_DIR = os.path.join(RESULT_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_screenshot(page, name):
    """Capture screenshot and store it in the timestamped folder"""
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path)
    return path
