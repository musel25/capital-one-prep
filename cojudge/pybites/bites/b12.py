"""Bite: Alternative constructors (recreated tests and template)."""

SPEC = {
    "title": "Alternative constructors",
    "module": "constructors",
    "template": '''import re


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:

    def __init__(self, name):
        # validate a current domain (r'.*\\.[a-z]{2,3}$' is fine)
        # if not valid, raise a DomainException
        self.name = name

    # next add a __str__ method and write 2 class methods
    # called parse_url and parse_email to construct domains
    # from an URL and email respectively
''',
    "tests": '''import pytest

from constructors import Domain, DomainException


@pytest.mark.parametrize("name", ["google.com", "pybit.es", "bbc.co.uk", "python.org"])
def test_valid_domain(name):
    domain = Domain(name)
    assert domain.name == name
    assert str(domain) == name


@pytest.mark.parametrize("name", ["google", "pybit.e", "pybites.comm", "python.org/", "python.42"])
def test_invalid_domain(name):
    with pytest.raises(DomainException):
        Domain(name)


@pytest.mark.parametrize("url, expected", [
    ("http://pybit.es", "pybit.es"),
    ("https://www.python.org/downloads/", "www.python.org"),
    ("https://docs.python.org/3/library/re.html?highlight=match#re.match", "docs.python.org"),
])
def test_parse_url(url, expected):
    domain = Domain.parse_url(url)
    assert type(domain) is Domain
    assert str(domain) == expected


@pytest.mark.parametrize("email, expected", [
    ("julian@pybit.es", "pybit.es"),
    ("bob@gmail.com", "gmail.com"),
])
def test_parse_email(email, expected):
    domain = Domain.parse_email(email)
    assert type(domain) is Domain
    assert str(domain) == expected


def test_parsed_domains_are_validated():
    with pytest.raises(DomainException):
        Domain.parse_url("http://localhost:8000/admin")
    with pytest.raises(DomainException):
        Domain.parse_email("root@localhost")


def test_classmethods_return_subclass_instances():
    class SubDomain(Domain):
        pass
    assert type(SubDomain.parse_url("http://pybit.es")) is SubDomain
    assert type(SubDomain.parse_email("bob@pybit.es")) is SubDomain
    assert isinstance(Domain.__dict__["parse_url"], classmethod)
    assert isinstance(Domain.__dict__["parse_email"], classmethod)
''',
    "reference": '''import re
from urllib.parse import urlparse


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:

    def __init__(self, name):
        if not re.match(r'.*\\.[a-z]{2,3}$', name):
            raise DomainException(f"invalid domain: {name!r}")
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def parse_url(cls, url):
        return cls(urlparse(url).netloc)

    @classmethod
    def parse_email(cls, email):
        return cls(email.split("@")[-1])
''',
}
