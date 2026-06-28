import time

from app.handlers.pingmyurls import PingMyUrlsHandler
from app.playwright.browser_manager import BrowserManager
from app.schemas.request import SubmissionRequest
from app.schemas.response import SubmissionResponse


class SubmissionOrchestrator:

    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResponse:

        start_time = time.perf_counter()
        print("STEP 1")
        browser_manager = BrowserManager(headless=False)

        try:
            print("STEP 2")
            await browser_manager.launch()
            print("STEP 3")
            handler = PingMyUrlsHandler(browser_manager)
            print("STEP 4")

            result = await handler.submit(request)
            print("STEP 5")

            total_time = round(
                time.perf_counter() - start_time,
                2,
            )

            return SubmissionResponse(
                total_sites=1,
                successful=1 if result.success else 0,
                failed=0 if result.success else 1,
                total_execution_time=total_time,
                results=[result],
            )

        finally:
            await browser_manager.shutdown()