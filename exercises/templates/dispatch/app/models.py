from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints

Text = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1, max_length=100)]
Weight = Annotated[int, Field(strict=True, ge=1, le=20000)]
Service = Literal['standard', 'express']


class Line(BaseModel):
    sku: Text
    quantity: Annotated[int, Field(strict=True, ge=1, le=20)]


class OrderRequest(BaseModel):
    customer: Text
    items: Annotated[list[Line], Field(min_length=1, max_length=10)]


class QuoteRequest(BaseModel):
    weights_grams: Annotated[list[Weight], Field(min_length=1, max_length=200)]
    service: Service
    signature: Annotated[bool, Field(strict=True)] = False


class ShipmentRequest(BaseModel):
    order_id: Text
    service: Service
    signature: Annotated[bool, Field(strict=True)] = False
