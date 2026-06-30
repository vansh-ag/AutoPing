import time

from app.captcha.hcaptcha_solver import HCaptchaSolver
from app.config.selectors import Selectors
from app.config.sites import Sites
from app.handlers.base_handler import BaseHandler
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult


class SmallSEOToolsHandler(BaseHandler):

    @property
    def site_name(self):
        return Sites.SMALLSEO["name"]

    @property
    def site_url(self):
        return Sites.SMALLSEO["url"]

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:

        start = time.perf_counter()

        context = None

        try:

            context, page = await self.browser_manager.new_page()

            print("\n" + "=" * 60)
            print("SMALLSEOTOOLS STARTED")
            print("=" * 60)

            #
            # Open Website
            #
            await page.goto(
                self.site_url,
                wait_until="domcontentloaded",
            )

            #
            # Fill URL
            #
            await page.fill(
                Selectors.SMALLSEO["url_input"],
                str(request.url),
            )

            print("✓ URL Filled")

            #
            # Click Ping
            #
            await page.click(
                Selectors.SMALLSEO["submit_button"],
            )

            print("✓ Ping Now Clicked")

            #
            # Give the page time to render the CAPTCHA.
            # Do NOT wait for networkidle because
            # ads and trackers keep the network busy.
            #
            await page.wait_for_timeout(3000)

            print(f"Current URL   : {page.url}")
            print(f"Current Title : {await page.title()}")

            #
            # Run hCaptcha Solver
            #
            solver = HCaptchaSolver()

            solved = await solver.solve(page)

            execution_time = round(
                time.perf_counter() - start,
                2,
            )

            return SubmissionResult(
                site=self.site_name,
                success=solved,
                message=(
                    "HCaptcha Solved"
                    if solved
                    else "HCaptcha Detected"
                ),
                execution_time=execution_time,
            )

        except Exception as e:

            execution_time = round(
                time.perf_counter() - start,
                2,
            )

            print("\n" + "=" * 60)
            print("SMALLSEOTOOLS ERROR")
            print(str(e))
            print("=" * 60)

            return SubmissionResult(
                site=self.site_name,
                success=False,
                message="Submission Failed",
                execution_time=execution_time,
                error=str(e),
            )

        finally:

            #
            # During Phase 3 debugging we intentionally
            # keep the browser open so we can inspect
            # the CAPTCHA.
            #
            if context:

                input("\nPress ENTER to close browser...")

                await self.browser_manager.close_context(
                    context
                )