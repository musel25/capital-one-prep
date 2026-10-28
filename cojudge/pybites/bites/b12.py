"""Bite: Alternative constructors (recreated tests and template)."""

SPEC = {
    "title": "Alternative constructors",
    "module": "constructors",
    "contract": "All inputs are strings. Direct domain names contain no whitespace. "
                "Use the template's simplified rule r'.*\\.[a-z]{2,3}$'; this is not full DNS validation. "
                "An empty name or a name that fails this rule raises DomainException. "
                "Keep accepted names unchanged. URLs use http or https, with a host and optional numeric port, "
                "path, query, or fragment. Validate the full network location, including its port if present; "
                "a numeric port therefore fails the domain rule. Credentials and malformed URLs are excluded. "
                "Emails have exactly one @ and a nonempty local part and domain part. Other email forms are excluded. "
                "Both classmethods extract the domain and use the same validation. Return an instance of the calling class. "
                "str(domain) returns its name. Other input types are excluded.",
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


@pytest.mark.parametrize('name', ['', 'a.b', 'a.abcd', 'a.COM'])
def test_domain_rule_boundaries(name):
    with pytest.raises(DomainException):
        Domain(name)


@pytest.mark.parametrize('name', ['a.io', 'a.xyz', 'sub.example.io'])
def test_short_names_and_subdomains(name):
    assert str(Domain(name)) == name


def test_url_and_email_keep_the_full_host():
    assert str(Domain.parse_url('https://sub.example.io/?q=other.com#other.org')) == 'sub.example.io'
    assert str(Domain.parse_email('first.last+tag@sub.example.io')) == 'sub.example.io'


def test_url_port_is_not_removed_before_validation():
    with pytest.raises(DomainException):
        Domain.parse_url('https://pybit.es:443/')


def test_invalid_domains_are_rejected_through_subclasses():
    class SubDomain(Domain):
        pass
    with pytest.raises(DomainException):
        SubDomain.parse_email('person@example.abcd')
    with pytest.raises(DomainException):
        SubDomain.parse_url('https://example.abcd/')
''',
    "mutations": [
        {"name": 'skip_domain_validation', "old": "if not re.match(r'.*\\.[a-z]{2,3}$', name):", "new": 'if False:'},
        {"name": 'url_returns_base_class', "old": 'return cls(urlparse(url).netloc)', "new": 'return Domain(urlparse(url).netloc)'},
        {"name": 'url_silently_strips_port', "old": 'return cls(urlparse(url).netloc)', "new": 'return cls(urlparse(url).hostname)'},
        {"name": 'email_loses_subdomain', "old": 'return cls(email.split("@")[-1])', "new": 'return cls(email.split("@")[-1].split(".", 1)[-1])'},
    ],
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
