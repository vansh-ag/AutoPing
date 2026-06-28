from abc import ABC, abstractmethod

from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult
from app.playwright.browser_manager import BrowserManager


class BaseHandler(ABC):
    """
    Base class for all ping website handlers.

    Every handler should:
    1. Open the website
    2. Fill the form
    3. Submit
    4. Verify success
    5. Return SubmissionResult
    """

    def __init__(self, browser_manager: BrowserManager):
        self.browser_manager = browser_manager

    @property
    @abstractmethod
    def site_name(self) -> str:
        """Human-readable site name."""
        pass

    @property
    @abstractmethod
    def site_url(self) -> str:
        """Target website URL."""
        pass

    @abstractmethod
    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:
        """
        Execute complete submission flow.
        """
        pass