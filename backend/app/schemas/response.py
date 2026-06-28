from typing import List

from pydantic import BaseModel

from app.schemas.result import SubmissionResult


class SubmissionResponse(BaseModel):
    """
    Final response returned to frontend.
    """

    total_sites: int

    successful: int

    failed: int

    total_execution_time: float

    results: List[SubmissionResult]