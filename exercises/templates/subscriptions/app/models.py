from datetime import date

from pydantic import BaseModel, Field


class QuoteRequest(BaseModel):
    target_plan: str = Field(min_length=1)
    effective_on: date
    cap_cents: int | None = Field(default=None, ge=0, strict=True)
