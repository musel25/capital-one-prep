from typing import Annotated
from pydantic import BaseModel, Field, model_validator

Cents = Annotated[int, Field(strict=True, gt=0)]


class Transfer(BaseModel):
    source: str
    target: str
    amount_cents: Cents

    @model_validator(mode='after')
    def different_accounts(self):
        if self.source == self.target:
            raise ValueError('Source and target must differ')
        return self


class Event(BaseModel):
    event_id: Annotated[str, Field(min_length=1)]
    amount_cents: Cents
