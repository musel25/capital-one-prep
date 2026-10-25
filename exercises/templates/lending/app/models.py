from pydantic import BaseModel, Field


class LoanRequest(BaseModel):
    equipment_id: str = Field(min_length=1)
    borrower: str = Field(min_length=1)
    quantity: int = Field(strict=True, gt=0)
