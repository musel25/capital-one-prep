"""Bite: Write a property. Original free template and tests, plus two added tests."""
import json
from pathlib import Path

_PAGE = {k: v.replace("\r\n", "\n") if isinstance(v, str) else v
         for k, v in json.loads((Path(__file__).parents[1] / "source-pages.json").read_text())[0].items()}

SPEC = {
    "title": "Write a property",
    "module": "simple_property",
    "original": True,
    "template": _PAGE["template"],
    "tests": _PAGE["tests"].rstrip() + '''


# Added for this course: `expired` is read-only and is computed on every access.

def test_expired_is_read_only():
    promo = Promo('old', NOW - timedelta(days=1))
    with pytest.raises(AttributeError):
        promo.expired = False


def test_expired_follows_a_new_date():
    promo = Promo('moving', NOW + timedelta(days=1))
    assert not promo.expired
    promo.expires = NOW - timedelta(days=1)
    assert promo.expired
''',
    "reference": '''from datetime import datetime

NOW = datetime.now()


class Promo:
    def __init__(self, name: str, expires: datetime):
        self.name = name
        self.expires = expires

    @property
    def expired(self) -> bool:
        return self.expires < NOW
''',
}
SPEC["tests"] = SPEC["tests"].replace("import inspect\n", "import inspect\n\nimport pytest\n", 1)

SPEC["contract"] = (
    "name is a string, including an empty string. expires is a naive datetime. "
    "Store both values. The read-only expired property returns a bool on each access: "
    "expires < the module's NOW. Equality is not expired. Changes to expires take effect "
    "on the next access. Other input types and timezone-aware datetimes are outside "
    "the contract; no validation is required for them."
)
SPEC["tests"] += '''


def test_expiry_boundary_and_boolean_result():
    assert Promo('equal', NOW).expired is False
    assert Promo('before', NOW - timedelta(microseconds=1)).expired is True
    assert Promo('after', NOW + timedelta(microseconds=1)).expired is False


def test_constructor_preserves_values_and_empty_name():
    promo = Promo('', NOW)
    assert promo.name == ''
    assert promo.expires == NOW


def test_expired_can_become_current_again():
    promo = Promo('extended', NOW - timedelta(days=1))
    assert promo.expired is True
    promo.expires = NOW + timedelta(days=1)
    assert promo.expired is False
'''
SPEC["mutations"] = [
    {"name": "expire at equality", "old": "self.expires < NOW", "new": "self.expires <= NOW"},
    {"name": "compare calendar dates only", "old": "self.expires < NOW", "new": "self.expires.date() < NOW.date()"},
    {"name": "discard promo name", "old": "self.name = name", "new": "self.name = 'promo'"},
]
