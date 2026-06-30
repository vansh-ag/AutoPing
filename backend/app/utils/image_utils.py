from pathlib import Path

from playwright.async_api import FrameLocator


class ImageUtils:

    SAVE_DIR = Path("screenshots")

    @classmethod
    async def save_hcaptcha(
        cls,
        frame: FrameLocator,
    ) -> str:

        cls.SAVE_DIR.mkdir(
            exist_ok=True,
        )

        image_path = cls.SAVE_DIR / "hcaptcha.png"

        await frame.locator("body").screenshot(
            path=str(image_path),
        )

        print(f"\n✓ Screenshot Saved : {image_path}")

        return str(image_path)