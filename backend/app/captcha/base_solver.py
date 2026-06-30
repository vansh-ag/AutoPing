from abc import ABC
from abc import abstractmethod

from playwright.async_api import Page


class BaseSolver(ABC):

    @abstractmethod
    async def solve(
        self,
        page: Page,
    ) -> bool:
        """
        Returns True if captcha solved.
        False otherwise.
        """

        pass