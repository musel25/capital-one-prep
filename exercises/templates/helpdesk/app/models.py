from typing import Annotated, Literal
from pydantic import BaseModel, StringConstraints

Text = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]


class Comment(BaseModel):
    author: Text
    body: Text


class StatusChange(BaseModel):
    actor: Text
    status: Literal['new', 'open', 'resolved']
