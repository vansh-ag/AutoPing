import time

from app.config.selectors import Selectors
from app.config.sites import Sites
from app.handlers.base_handler import BaseHandler
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult
from app.verification.success_checker import SuccessChecker


class PingMyUrlsHandler(BaseHandler):

    @property
    def site_name(self) -> str:
        return Sites.PING_MY_URLS["name"]

    @property
    def site_url(self) -> str:
        return Sites.PING_MY_URLS["url"]

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:

        start_time = time.perf_counter()

        context = None

        try:

            context, page = await self.browser_manager.new_page()

            # Open Website
            await page.goto(
                self.site_url,
                wait_until="domcontentloaded",
            )

            # Wait until URL input is visible
            await page.locator(
                Selectors.PING_MY_URLS["url_input"]
            ).wait_for()

            # Fill URL
            await page.locator(
                Selectors.PING_MY_URLS["url_input"]
            ).fill(str(request.url))

            # Click Submit
            await page.get_by_role(
                "button",
                name=Selectors.PING_MY_URLS["submit_button_role"],
            ).click()

            # Wait for processing
            await page.wait_for_timeout(5000)

            # Verify
            success, message = await SuccessChecker.verify(page)

            screenshot = await SuccessChecker.take_screenshot(
                page,
                "pingmyurls.png",
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
                await self.browser_manager.close_context(context)