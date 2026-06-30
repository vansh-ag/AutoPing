import asyncio

from app.captcha.manager import CaptchaManager
from app.playwright.browser_manager import BrowserManager


TEST_URL = "https://smallseotools.com/online-ping-website-tool/"


async def main():

    print("=" * 60)
    print("PHASE 3A - CAPTCHA DETECTOR TEST")
    print("=" * 60)

    browser = BrowserManager(headless=False)

    await browser.launch()

    context, page = await browser.new_page()

    try:

        print("\nOpening Website...")

        await page.goto(
            TEST_URL,
            wait_until="domcontentloaded",
        )

        #
        # Fill URL
        #
        print("Filling URL...")

        await page.get_by_role(
            "textbox",
            name="Enter URLs",
        ).fill("https://example.com")

        #
        # Submit
        #
        print("Clicking Ping Now...")

        await page.get_by_role(
            "button",
            name="Ping Now",
        ).click()

        #
        # Wait for possible captcha
        #
        print("Waiting for CAPTCHA...")

        await page.wait_for_timeout(2500)

        #
        # Detect CAPTCHA
        #
        manager = CaptchaManager()

        captcha = await manager.detect(page)

        print("\nResult:")
        print(f"Captcha Type : {captcha.value}")

        print("\nBrowser will remain open.")
        input("Press ENTER to close...")

    finally:

        await browser.close_context(context)

        await browser.shutdown()


if __name__ == "__main__":
    asyncio.run(main())