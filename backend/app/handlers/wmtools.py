import time

from app.config.selectors import Selectors
from app.config.sites import Sites
from app.handlers.base_handler import BaseHandler
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult
from app.verification.success_checker import SuccessChecker


class WMToolsHandler(BaseHandler):

    @property
    def site_name(self):
        return Sites.WMTOOLS["name"]

    @property
    def site_url(self):
        return Sites.WMTOOLS["url"]

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:

        start = time.perf_counter()

        context = None

        try:

            context, page = await self.browser_manager.new_page()

            print("=" * 60)
            print("WMTOOLS STARTED")
            print("=" * 60)

            await page.goto(
                self.site_url,
                wait_until="domcontentloaded",
            )

            #
            # Fill URL
            #
            await page.fill(
                Selectors.WMTOOLS["url_input"],
                str(request.url),
            )

            print("✓ URL Filled")

            await page.wait_for_timeout(1000)

            print("About to click PING")

            #
            # Submit
            #
            await page.get_by_role(
                "button",
                name="PING",
                exact=True,
            ).click(force=True)

            print("✓ PING Clicked")

            await page.wait_for_load_state(
                "domcontentloaded"
            )

            await page.wait_for_timeout(3000)

            print(f"Current URL : {page.url}")
            print(f"Current Title : {await page.title()}")

            success, message = await SuccessChecker.verify(
                page
            )

            screenshot = await SuccessChecker.take_screenshot(
                page,
                "wmtools.png",
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

            print("=" * 60)
            print("WMTOOLS ERROR")
            print(e)
            print("=" * 60)

            execution_time = round(
                time.perf_counter() - start,
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