from typing import Annotated
from pydantic import BaseModel, StringConstraints

Text = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]


class LoanRequest(BaseModel):
    book_id: Text
    reader: Text
