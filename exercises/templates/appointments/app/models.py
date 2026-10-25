from datetime import date
from typing import Literal
from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    provider_id: str = Field(min_length=1)
    on: date
    start: str = Field(pattern=r'^(?:[01][0-9]|2[0-3]):[0-5][0-9]$')
    duration_minutes: Literal[30, 60] = 30
