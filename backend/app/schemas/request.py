from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SubmissionRequest(BaseModel):
    """
    Request received from the frontend.
    Only URL is mandatory.
    Remaining fields are optional because
    different ping websites require different inputs.
    """

    url: HttpUrl = Field(
        ...,
        description="Website URL to submit",
        examples=["https://example.com"],
    )

    title: Optional[str] = Field(
        default=None,
        description="Website title or blog title",
        max_length=255,
    )

    rss_url: Optional[HttpUrl] = Field(
        default=None,
        description="RSS Feed URL (required only by some services)",
    )

    category: Optional[str] = Field(
        default=None,
        description="Website category if required",
    )

    email: Optional[str] = Field(
        default=None,
        description="Optional email address",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "title": "Example Website",
                "rss_url": "https://example.com/rss.xml",
                "category": "Technology",
                "email": "admin@example.com",
            }
        }