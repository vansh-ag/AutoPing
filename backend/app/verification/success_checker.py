from pathlib import Path
from typing import Tuple

from playwright.async_api import Page


class SuccessChecker:
    """
    Centralized submission verification.

    Every handler should use this class instead of
    implementing its own success detection logic.
    """

    SUCCESS_KEYWORDS = [
        "success",
        "submitted",
        "submission successful",
        "ping sent",
        "completed",
        "thank you",
        "accepted",
        "done",
    ]

    ERROR_KEYWORDS = [
        "error",
        "failed",
        "invalid",
        "required",
        "captcha",
        "try again",
    ]

    @staticmethod
    async def verify(page: Page) -> Tuple[bool, str]:
        """
        Verifies whether a submission was successful.

        Returns:
            (success, message)
        """

        try:
            body = await page.locator("body").inner_text()

            body = body.lower()

            for keyword in SuccessChecker.SUCCESS_KEYWORDS:
                if keyword in body:
                    return True, f"Success keyword detected: '{keyword}'"

            for keyword in SuccessChecker.ERROR_KEYWORDS:
                if keyword in body:
                    return False, f"Error keyword detected: '{keyword}'"

            return False, "Unable to verify submission."

        except Exception as e:
            return False, str(e)

    @staticmethod
    async def take_screenshot(
        page: Page,
        file_name: str,
    ) -> str:
        """
        Saves a screenshot for debugging.

        Returns:
            Screenshot path
        """

        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        path = screenshots_dir / file_name

        await page.screenshot(
            path=str(path),
            full_page=True,
        )

        return str(path)