from playwright.async_api import Page

from app.captcha.captcha_type import CaptchaType
from app.captcha.detector import CaptchaDetector


class CaptchaManager:
    """
    Phase 3A

    Responsible only for detecting CAPTCHA.
    Solving will be added in Phase 3B.
    """

    async def detect(
        self,
        page: Page,
    ) -> CaptchaType:

        captcha = await CaptchaDetector.detect(page)

        print("\n" + "=" * 60)
        print(f"CAPTCHA DETECTED : {captcha.value.upper()}")
        print("=" * 60 + "\n")

        return captcha