from typing import Literal
from pydantic import BaseModel, Field


class ReadingRequest(BaseModel):
    service_id: str = Field(min_length=1)
    duration_us: int = Field(strict=True, ge=0)
    status: Literal['ok', 'error']
