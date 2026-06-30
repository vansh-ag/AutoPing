from abc import ABC, abstractmethod

from app.captcha.manager import CaptchaManager
from app.playwright.browser_manager import BrowserManager
from app.schemas.request import SubmissionRequest
from app.schemas.result import SubmissionResult


class BaseHandler(ABC):
    """
    Base class for every website handler.

    Responsibilities:
    - Store BrowserManager
    - Store CaptchaManager
    - Provide common interface for handlers
    """

    def __init__(
        self,
        browser_manager: BrowserManager,
    ) -> None:

        self.browser_manager = browser_manager

        self.captcha_manager = CaptchaManager()

    @property
    @abstractmethod
    def site_name(self) -> str:
        """
        Human-readable website name.
        """
        pass

    @property
    @abstractmethod
    def site_url(self) -> str:
        """
        Website URL.
        """
        pass

    @abstractmethod
    async def submit(
        self,
        request: SubmissionRequest,
    ) -> SubmissionResult:
        """
        Execute complete submission workflow.
        """
        pass