import time

from playwright.async_api import Page

from app.config.selectors import Selectors
from app.utils.image_utils import ImageUtils


class HCaptchaSolver:

    async def solve(
        self,
        page: Page,
    ) -> bool:

        print("\n" + "=" * 60)
        print("HCAPTCHA SOLVER")
        print("=" * 60)

        #
        # Wait for hCaptcha up to 15 seconds.
        #
        iframe_count = 0

        for second in range(15):

            iframe_count = await page.locator(
                Selectors.HCAPTCHA["iframe"]
            ).count()

            print(
                f"Searching hCaptcha... {second + 1}/15"
            )

            if iframe_count > 0:
                break

            await page.wait_for_timeout(1000)

        print(f"\niframe count : {iframe_count}")

        if iframe_count == 0:

            print("❌ No hCaptcha Found")

            return False

        print("✅ hCaptcha Found")

        #
        # Print Frames
        #
        print("\nPAGE FRAMES\n")

        for index, frame in enumerate(page.frames):

            print(f"[{index}] {frame.url}")

        #
        # Create Frame Locator
        #
        frame = page.frame_locator(
            Selectors.HCAPTCHA["iframe"]
        )

        print("\n✓ Frame Located")

        #
        # Save Screenshot
        #
        screenshot = await ImageUtils.save_hcaptcha(
            frame
        )

        print(f"Saved : {screenshot}")

        #
        # Phase 3A ends here.
        #
        return False