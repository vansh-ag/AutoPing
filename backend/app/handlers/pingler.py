import time

from app.config.selectors import Selectors
from app.config.sites import Sites
from app.handlers.base_handler import BaseHandler
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult
from app.verification.success_checker import SuccessChecker


class PinglerHandler(BaseHandler):

    @property
    def site_name(self):
        return Sites.PINGLER["name"]

    @property
    def site_url(self):
        return Sites.PINGLER["url"]

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:

        start = time.perf_counter()

        context = None

        try:

            context, page = await self.browser_manager.new_page()

            print("=" * 60)
            print("PINGLER STARTED")
            print("=" * 60)

            #
            # Open Website
            #
            await page.goto(
                self.site_url,
                wait_until="domcontentloaded",
            )

            #
            # Pause Advertisement (optional)
            #
            try:

                ad_frame = page.frame_locator(
                    Selectors.PINGLER["ad_iframe"]
                )

                await ad_frame.get_by_role(
                    "button",
                    name="Pause",
                ).click(
                    timeout=3000,
                )

                print("✓ Advertisement Paused")

            except Exception:

                print("Advertisement not found (continuing...)")

            #
            # Fill Title
            #
            await page.fill(
                Selectors.PINGLER["title_input"],
                request.title or "Example Website",
            )

            print("✓ Title Filled")

            #
            # Fill URL
            #
            await page.fill(
                Selectors.PINGLER["url_input"],
                str(request.url),
            )

            print("✓ URL Filled")

            #
            # Select Category = Other
            #
            await page.check(
                Selectors.PINGLER["other_checkbox"],
            )

            print("✓ Category Selected")

            #
            # Submit
            #
            print("About to click Ping!")

            await page.click(
                Selectors.PINGLER["submit_button"],
            )

            print("✓ Ping Clicked")

            #
            # Wait a few seconds.
            # Pingler starts its cooldown timer
            # immediately after accepting submission.
            #
            await page.wait_for_timeout(3000)

            print(f"Current URL : {page.url}")
            print(f"Current Title : {await page.title()}")

            success, message = await SuccessChecker.verify(page)

            screenshot = await SuccessChecker.take_screenshot(
                page,
                "pingler.png",
            )

            execution_time = round(
                time.perf_counter() - start,
                2,
            )

            return SubmissionResult(
                site=self.site_name,
                success=success,
                message=message,
                execution_time=execution_time,
                screenshot=screenshot,
            )

        except Exception as e:

            execution_time = round(
                time.perf_counter() - start,
                2,
            )

            print("=" * 60)
            print("PINGLER ERROR")
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

            if context:
                await self.browser_manager.close_context(
                    context
                )