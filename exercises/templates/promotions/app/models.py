from datetime import datetime
from typing import Annotated
from pydantic import AwareDatetime, BaseModel, Field, StrictBool


class Purchase(BaseModel):
    at: AwareDatetime
    amount_cents: Annotated[int, Field(strict=True, gt=0)]
    active_member: StrictBool
