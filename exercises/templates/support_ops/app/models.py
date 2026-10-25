from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints

Text = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1, max_length=200)]


class CommentRequest(BaseModel):
    actor: Text
    body: Text


class StatusRequest(BaseModel):
    actor: Text
    status: Literal['open', 'resolved']


class AssignmentRequest(BaseModel):
    ticket_ids: Annotated[list[Text], Field(min_length=1, max_length=10)]
    agent_id: Text
    actor: Text
