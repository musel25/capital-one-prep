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
from urllib.parse import urlparse

# What you practise
# -----------------
# An alternative constructor is a @classmethod that builds an object from a
# different kind of input. A class method gets the CLASS as its first
# argument, called cls, and returns cls(...):
#
#     @classmethod
#     def parse_email(cls, email):
#         return cls(<the domain part of email>)
#
#     Domain.parse_email('bob@gmail.com')  -> Domain('gmail.com')
#
# Use cls(...), not Domain(...). Then a subclass gets an object of its own
# type: SubDomain.parse_email(...) returns a SubDomain.
#
# SUPPLIED: the three helpers below do the regex, URL and email work. They are
# not the skill of this exercise. Use them. Do not edit them.
#
# Work in four steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (validate in __init__)  -> test_invalid_domain
#   Step 2 (__str__)               -> test_valid_domain
#   Step 3 (parse_url)             -> test_parse_url
#   Step 4 (parse_email)           -> test_parse_email and the tests after it


def _is_valid_domain(name):
    """True for names such as 'pybit.es': text, a dot, 2 or 3 lowercase letters."""
    return re.fullmatch(r'.*\\.[a-z]{2,3}', name) is not None


def _host_of_url(url):
    """'https://pybit.es/articles/?q=1' -> 'pybit.es' (a port stays: 'pybit.es:443')."""
    return urlparse(url).netloc


def _domain_of_email(email):
    """'julian@pybit.es' -> 'pybit.es'"""
    return email.split('@')[-1]


class DomainException(Exception):
    """Raised when an invalid domain is created."""


class Domain:

    # Step 1: reject invalid names before you store them.
    #
    #     Domain('pybit.es').name  -> 'pybit.es'
    #     Domain('google')         -> raises DomainException (no dot)
    #     Domain('a.COM')          -> raises DomainException (uppercase ending)
    def __init__(self, name):
        # TODO: if not _is_valid_domain(name), raise DomainException.
        self.name = name

    # Step 2:  str(Domain('pybit.es'))  -> 'pybit.es'
    #
    # TODO: define __str__(self). It returns self.name.

    # Step 3: build a Domain from a URL. The host is the domain.
    #
    #     Domain.parse_url('https://www.python.org/downloads/')  -> Domain('www.python.org')
    #     Domain.parse_url('http://localhost:8000/admin')        -> raises DomainException
    #         (the constructor checks the name, so you get this for free)
    #
    # TODO: put @classmethod on the line above, then
    #       def parse_url(cls, url): return cls(<_host_of_url(url)>)

    # Step 4: build a Domain from an email address.
    #
    #     Domain.parse_email('julian@pybit.es')  -> Domain('pybit.es')
    #
    # TODO: put @classmethod on the line above, then
    #       def parse_email(cls, email): return cls(<_domain_of_email(email)>)
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
    "hints": [
        "Focus: @classmethod. The method gets the class as cls and returns cls(...). Do not write Domain(...) inside it.",
        "Supplied: _is_valid_domain, _host_of_url and _domain_of_email do the regex, URL and email work. Use them.",
        "parse_url is one line: return cls(_host_of_url(url)). The constructor then validates the name.",
    ],
    "mutations": [
        {"name": 'skip_domain_validation', "old": "if not _is_valid_domain(name):", "new": 'if False:'},
        {"name": 'url_returns_base_class', "old": 'return cls(_host_of_url(url))', "new": 'return Domain(_host_of_url(url))'},
        {"name": 'email_returns_base_class', "old": 'return cls(_domain_of_email(email))', "new": 'return Domain(_domain_of_email(email))'},
        {"name": 'url_bypasses_validation', "old": 'return cls(_host_of_url(url))', "new": 'obj = cls.__new__(cls); obj.name = _host_of_url(url); return obj'},
        {"name": 'str_returns_repr', "old": 'return self.name', "new": 'return repr(self.name)'},
    ],
    "reference": r'''import re
from urllib.parse import urlparse

# FOCUS: write __str__ and the two classmethods by hand.
#        A classmethod gets the class as `cls` and returns cls(...),
#        so a subclass gets an instance of the subclass.
# SUPPLIED: the three helpers below do the regex, URL and email work.
#        They are not the skill of this exercise. Use them. Do not edit them.


def _is_valid_domain(name):
    """True for names such as 'pybit.es': text, a dot, 2 or 3 lowercase letters."""
    return re.fullmatch(r'.*\.[a-z]{2,3}', name) is not None


def _host_of_url(url):
    """'https://pybit.es/articles/?q=1' -> 'pybit.es' (a port stays: 'pybit.es:443')."""
    return urlparse(url).netloc


def _domain_of_email(email):
    """'julian@pybit.es' -> 'pybit.es'"""
    return email.split('@')[-1]


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:

    def __init__(self, name):
        if not _is_valid_domain(name):
            raise DomainException(f"invalid domain: {name!r}")
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def parse_url(cls, url):
        return cls(_host_of_url(url))

    @classmethod
    def parse_email(cls, email):
        return cls(_domain_of_email(email))
''',
}

SPEC["hints"] = [
    'Concept: @classmethod gives the method the class as cls instead of an object as self. An alternative constructor returns cls(...), so Domain.parse_url returns a Domain and SubDomain.parse_url returns a SubDomain.',
    'Put the check in __init__ only: if not _is_valid_domain(name): raise DomainException(name). Both class methods call cls(...), so the constructor validates their result too.',
    'Each class method is one line: return cls(_host_of_url(url)) and return cls(_domain_of_email(email)). A test fails if you write Domain(...) instead of cls(...).',
]
