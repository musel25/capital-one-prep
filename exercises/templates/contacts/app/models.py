import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class ContactRequest(BaseModel):
    name: str
    email: str
    team: Literal['events', 'support']

    @field_validator('name')
    @classmethod
    def name_required(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('Name is required')
        return value

    @field_validator('email')
    @classmethod
    def email_address(cls, value):
        value = value.strip().lower()
        if not re.fullmatch(r'[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+', value):
            raise ValueError('Use an email address with a dotted domain')
        return value


class ImportRequest(BaseModel):
    contacts: list[ContactRequest] = Field(min_length=1, max_length=50)
