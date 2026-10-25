from datetime import date
from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel, Field, StringConstraints


def calendar_month(value):
    date.fromisoformat(f'{value}-01')
    return value


Month = Annotated[str, StringConstraints(pattern=r'^[0-9]{4}-(0[1-9]|1[0-2])$'), AfterValidator(calendar_month)]
Identifier = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class UsageEvent(BaseModel):
    event_id: Identifier
    workspace_id: Identifier
    month: Month
    meter_id: Identifier
    sample_id: Identifier
    units: int = Field(strict=True, gt=0)
    status: Literal['accepted', 'pending', 'rejected']
