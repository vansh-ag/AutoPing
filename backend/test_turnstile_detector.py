import asyncio

from app.playwright.browser_manager import BrowserManager
from app.captcha.manager import CaptchaManager


async def main():

    browser = BrowserManager(headless=False)

    await browser.launch()

    context, page = await browser.new_page()

    await page.goto(
        "https://2captcha.com/demo/cloudflare-turnstile",
        wait_until="domcontentloaded",
    )

    await page.wait_for_timeout(3000)

    manager = CaptchaManager()

    captcha = await manager.detect(page)

    print(f"\nDetected : {captcha.value}")

    input("\nPress ENTER to close...")

    await browser.close_context(context)

    await browser.shutdown()


if __name__ == "__main__":
    asyncio.run(main())