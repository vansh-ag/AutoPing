import time

from app.config.selectors import Selectors
from app.config.sites import Sites
from app.handlers.base_handler import BaseHandler
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult
from app.verification.success_checker import SuccessChecker


class BulkLinkHandler(BaseHandler):

    @property
    def site_name(self):
        return Sites.BULKLINK["name"]

    @property
    def site_url(self):
        return Sites.BULKLINK["url"]

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:

        start = time.perf_counter()

        context = None

        try:

            context, page = await self.browser_manager.new_page()

            print("=" * 60)
            print("BULKLINK STARTED")
            print("=" * 60)

            await page.goto(
                self.site_url,
                wait_until="domcontentloaded",
            )

            #
            # Fill URL
            #
            await page.fill(
                Selectors.BULKLINK["url_input"],
                str(request.url),
            )

            print("✓ URL Filled")

            #
            # Search Select All
            #
            await page.click(
                Selectors.BULKLINK["search_all"]
            )

            print("✓ Search Engines Selected")

            #
            # Ping Select All
            #
            await page.click(
                Selectors.BULKLINK["ping_all"]
            )

            print("✓ Ping Services Selected")

            #
            # Whois
            #
            await page.get_by_role(
                "checkbox",
                name="WhoIs Sites",
            ).check()

            print("✓ Whois Selected")

            #
            # About Info
            #
            await page.get_by_role(
                "checkbox",
                name="About & Info Pages",
            ).check()

            print("✓ About Pages Selected")

            await page.wait_for_timeout(1000)

            print("About to Submit")

            #
            # Submit
            #
            await page.get_by_role(
                "button",
                name="Submit URLs",
            ).click(force=True)

            print("✓ Submit Clicked")

            await page.wait_for_load_state(
                "domcontentloaded"
            )

            await page.wait_for_timeout(3000)

            print(page.url)

            print(await page.title())

            success, message = await SuccessChecker.verify(
                page
            )

            screenshot = (
                await SuccessChecker.take_screenshot(
                    page,
                    "bulklink.png",
                )
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
            print("BULKLINK ERROR")
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