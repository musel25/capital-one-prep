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
