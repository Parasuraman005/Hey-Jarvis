
from pathlib import Path
from datetime import datetime
import pyautogui


class ScreenshotController:

    def __init__(self):
        self.folder = Path.home() / "Pictures" / "JARVIS"
        self.folder.mkdir(parents=True, exist_ok=True)

    def take_screenshot(self):

        try:
            filename = datetime.now().strftime(
                "Screenshot_%Y%m%d_%H%M%S.png"
            )

            filepath = self.folder / filename

            image = pyautogui.screenshot()
            image.save(filepath)

            return f"Screenshot saved successfully: {filepath}"

        except Exception as error:
            return f"Screenshot failed: {error}"
