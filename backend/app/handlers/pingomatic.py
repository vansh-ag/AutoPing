import time

from app.config.selectors import Selectors
from app.config.sites import Sites
from app.handlers.base_handler import BaseHandler
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult
from app.verification.success_checker import SuccessChecker


class PingomaticHandler(BaseHandler):

    @property
    def site_name(self) -> str:
        return Sites.PINGOMATIC["name"]

    @property
    def site_url(self) -> str:
        return Sites.PINGOMATIC["url"]

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:

        start_time = time.perf_counter()

        context = None

        try:

            context, page = await self.browser_manager.new_page()

            print("=" * 60)
            print("PINGOMATIC STARTED")
            print("=" * 60)

            await page.goto(
                self.site_url,
                wait_until="domcontentloaded",
            )

            #
            # Fill Blog Name
            #
            await page.fill(
                Selectors.PINGOMATIC["blog_name"],
                request.title or "AutoPing",
            )

            print("✓ Blog Name Filled")

            #
            # Fill Homepage
            #
            await page.fill(
                Selectors.PINGOMATIC["homepage"],
                str(request.url),
            )

            print("✓ Homepage Filled")

            #
            # Fill RSS URL (Optional)
            #
            if request.rss_url:

                await page.fill(
                    Selectors.PINGOMATIC["rss_url"],
                    str(request.rss_url),
                )

            print("✓ RSS Filled")

            #
            # Enable Blo.gs
            #
            await page.get_by_role(
                "checkbox",
                name="Blo.gs",
            ).check()

            print("✓ Blo.gs Checked")

            #
            # Enable Feed Burner
            #
            await page.get_by_role(
                "checkbox",
                name="Feed Burner",
            ).check()

            print("✓ Feed Burner Checked")

            #
            # Let page stabilize
            #
            await page.wait_for_timeout(1000)

            print("About to click Send Pings")

            #
            # Submit
            #
            await page.get_by_role(
                "link",
                name="Send Pings »",
            ).click(force=True)

            print("✓ Send Pings Clicked")

            #
            # Wait for navigation
            #
            await page.wait_for_load_state(
                "domcontentloaded"
            )

            await page.wait_for_timeout(3000)

            print(f"Current URL : {page.url}")

            print(
                f"Current Title : {await page.title()}"
            )

            #
            # Verify
            #
            success, message = await SuccessChecker.verify(
                page
            )

            screenshot = (
                await SuccessChecker.take_screenshot(
                    page,
                    "pingomatic.png",
                )
            )

            execution_time = round(
                time.perf_counter() - start_time,
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

            print("=" * 60)
            print("PINGOMATIC ERROR")
            print(e)
            print("=" * 60)

            execution_time = round(
                time.perf_counter() - start_time,
                2,
            )

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