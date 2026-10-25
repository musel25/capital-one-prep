from typing import Literal

from pydantic import BaseModel, Field


class ExportRequest(BaseModel):
    dataset_id: str = Field(min_length=1)
    format: Literal['csv', 'json']
