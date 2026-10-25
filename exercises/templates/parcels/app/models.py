from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints, StrictBool


class QuoteRequest(BaseModel):
    zone: Annotated[str, StringConstraints(strict=True, min_length=1)]
    service: Literal['standard', 'express']
    weight_grams: Annotated[int, Field(strict=True, ge=1, le=20000)]
    signature: StrictBool = False
