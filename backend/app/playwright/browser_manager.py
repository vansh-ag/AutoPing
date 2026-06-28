from typing import Optional

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)


class BrowserManager:
    """
    Responsible for managing the Playwright lifecycle.

    Responsibilities:
    - Start Playwright
    - Launch Chromium
    - Create isolated browser contexts
    - Create pages
    - Close browser cleanly

    Every website handler should use this class.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless

        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None

    async def launch(self) -> None:
        """
        Starts Playwright and launches Chromium.
        """

        if self.browser is not None:
            return

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=self.headless
        )

    async def new_context(self) -> BrowserContext:
        """
        Creates an isolated browser context.

        Each website gets its own context so
        cookies/session data don't interfere.
        """

        if self.browser is None:
            raise RuntimeError("Browser has not been launched.")

        context = await self.browser.new_context()

        return context

    async def new_page(self) -> tuple[BrowserContext, Page]:
        """
        Creates a new page inside a fresh browser context.
        """

        context = await self.new_context()

        page = await context.new_page()

        page.set_default_timeout(30000)

        page.set_default_navigation_timeout(30000)

        return context, page

    async def close_context(
        self,
        context: BrowserContext,
    ) -> None:
        """
        Closes a browser context.
        """

        await context.close()

    async def shutdown(self) -> None:
        """
        Properly closes browser and Playwright.
        """

        if self.browser is not None:
            await self.browser.close()

        if self.playwright is not None:
            await self.playwright.stop()

        self.browser = None
        self.playwright = None