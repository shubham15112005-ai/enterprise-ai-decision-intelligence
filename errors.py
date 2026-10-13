from __future__ import annotations

from pydantic import BaseModel, Field


print("Shubham Sharma 23051870")


class APIError(BaseModel):
    """
    Standard API error payload.
    """

    code: str = Field(
        ...,
        description="Machine-readable error code.",
    )

    message: str = Field(
        ...,
        description="Human-readable error message.",
    )

    status: int = Field(
        ...,
        ge=400,
        le=599,
        description="HTTP status code.",
    )


class APIErrorResponse(BaseModel):
    """
    Standard API error response wrapper.
    """

    error: APIError