from playwright.async_api import Page

from app.captcha.captcha_type import CaptchaType


class CaptchaDetector:

    @staticmethod
    async def detect(
        page: Page,
    ) -> CaptchaType:

        turnstile = await page.locator(
            "iframe[src*='turnstile']"
        ).count()

        hcaptcha = await page.locator(
            "iframe[src*='hcaptcha']"
        ).count()

        recaptcha = await page.locator(
            "iframe[src*='recaptcha']"
        ).count()

        image_alt = await page.locator(
            "img[alt*='captcha']"
        ).count()

        image_src = await page.locator(
            "img[src*='captcha']"
        ).count()

        print("\n===== CAPTCHA DEBUG =====")

        print("Turnstile :", turnstile)

        print("HCaptcha  :", hcaptcha)

        print("Recaptcha :", recaptcha)

        print("Image Alt :", image_alt)

        print("Image Src :", image_src)

        print("=========================\n")

        if turnstile > 0:
            return CaptchaType.TURNSTILE

        if hcaptcha > 0:
            return CaptchaType.HCAPTCHA

        if recaptcha > 0:
            return CaptchaType.RECAPTCHA

        if image_alt > 0 or image_src > 0:
            return CaptchaType.IMAGE

        return CaptchaType.NONE