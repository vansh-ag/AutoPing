from fastapi import APIRouter, HTTPException

from app.schemas.request import SubmissionRequest
from app.schemas.response import SubmissionResponse
from app.orchestrator.submission_orchestrator import SubmissionOrchestrator

router = APIRouter()


@router.post(
    "/submit",
    response_model=SubmissionResponse,
    summary="Submit URL to Ping Services",
)
async def submit_url(request: SubmissionRequest):
    """
    Receives a submission request from the frontend.

    Current Phase:
        - Calls only PingMyUrls Handler.

    Future Phases:
        - Parallel execution across all supported ping services.
        - CAPTCHA solving.
        - Retry mechanism.
        - Report generation.
    """

    try:
        orchestrator = SubmissionOrchestrator()

        result = await orchestrator.submit(request)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Submission failed: {str(e)}",
        )
    