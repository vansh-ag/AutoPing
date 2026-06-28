from typing import Optional

from pydantic import BaseModel


class SubmissionResult(BaseModel):
    """
    Result returned by a single website handler.
    """

    site: str

    success: bool

    message: str

    execution_time: float

    screenshot: Optional[str] = None

    error: Optional[str] = None