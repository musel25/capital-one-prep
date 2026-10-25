from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints


class Line(BaseModel):
    sku: Annotated[str, StringConstraints(strict=True, min_length=1)]
    quantity: Annotated[int, Field(strict=True, ge=1, le=100)]


class InvoicePreview(BaseModel):
    lines: Annotated[list[Line], Field(min_length=1)]
    discount_percent: Annotated[int, Field(strict=True, ge=0, le=100)] = 0
