from typing import Annotated
from pydantic import BaseModel, Field


class Item(BaseModel):
    sku: str
    quantity: Annotated[int, Field(strict=True, gt=0)]


class Reservation(BaseModel):
    items: Annotated[list[Item], Field(min_length=1)]
