import time

from app.handlers.pingmyurls import PingMyUrlsHandler
from app.handlers.pingomatic import PingomaticHandler

from app.playwright.browser_manager import BrowserManager

from app.schemas.request import SubmissionRequest
from app.schemas.response import SubmissionResponse
from app.handlers.bulklink import BulkLinkHandler

class SubmissionOrchestrator:

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResponse:

        start_time = time.perf_counter()

        browser_manager = BrowserManager(
            headless=False
        )

        try:

            print("Launching browser...")
            await browser_manager.launch()

            handlers = [

                PingMyUrlsHandler(browser_manager),

                PingomaticHandler(browser_manager),

                BulkLinkHandler(browser_manager),

            ]

            results = []

            for handler in handlers:

                print(f"Running {handler.site_name}")

                result = await handler.submit(request)

                results.append(result)

            total_time = round(
                time.perf_counter() - start_time,
                2,
            )

            successful = sum(1 for r in results if r.success)
            failed = len(results) - successful

            return SubmissionResponse(
                total_sites=len(results),
                successful=successful,
                failed=failed,
                total_execution_time=total_time,
                results=results,
            )

        finally:

            print("Closing browser...")

            await browser_manager.shutdown()