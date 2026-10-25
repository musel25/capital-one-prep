from datetime import date
from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel, Field, StringConstraints


def calendar_month(value):
    date.fromisoformat(f'{value}-01')
    return value


Month = Annotated[str, StringConstraints(pattern=r'^[0-9]{4}-(0[1-9]|1[0-2])$'), AfterValidator(calendar_month)]


class ExpenseRequest(BaseModel):
    employee_id: str = Field(min_length=1)
    incurred_on: date
    category: Literal['meals', 'supplies', 'travel']
    amount_cents: int = Field(strict=True, gt=0)
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
