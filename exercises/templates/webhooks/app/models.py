from typing import Literal

from pydantic import BaseModel, Field


class DeliveryEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=80)
    parcel_id: str = Field(min_length=1)
    status: Literal['arrived', 'delayed']
