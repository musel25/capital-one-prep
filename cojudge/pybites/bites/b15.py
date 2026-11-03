"""Bite: Abc's and class inheritance (recreated tests and template)."""

SPEC = {
    "title": "Abc's and class inheritance",
    "module": "challenge",
    "contract": "Challenge takes an int number and str title. Empty titles and zero or negative numbers are allowed. "
                "Do not normalize or validate them. Challenge is abstract; verify and the pretty_title property "
                "must both be implemented before a subclass can be instantiated. Subclass constructors call super(). "
                "BlogChallenge takes a list of int PR numbers, including an empty list; verify checks membership. "
                "BiteChallenge takes a result and verifies it with ==, including falsy or unhashable built-in values. "
                "pretty_title formats the current number and title as 'PCCN - TITLE' or 'Bite N. TITLE'. "
                "Other number, title, and PR container types are outside this exercise.",
    "template": '''from abc import ABC, abstractmethod

# What you practise
# -----------------
# An abstract base class (ABC) describes an API: the methods and properties that
# every subclass MUST provide. Mark a member with @abstractmethod and Python
# refuses to create an object of a class that still has that member abstract:
# calling the class raises TypeError. A subclass becomes usable only after it
# overrides EVERY abstract member.
#
# Work in three steps. The tests run top to bottom, so finish each step before
# the next one. Then Submit runs the edge-case tests too.
#
#   Step 1 (Challenge)      -> test_base_class_is_abstract,
#                              test_subclass_must_implement_the_api
#   Step 2 (BlogChallenge)  -> test_blog_challenge
#   Step 3 (BiteChallenge)  -> test_bite_challenge


# Step 1: the abstract base class.
# Challenge(1, 'title') must raise TypeError after this step.
class Challenge(ABC):

    def __init__(self, number, title):
        # TODO: store number as self.number and title as self.title.
        ...

    # TODO: make verify abstract. Put @abstractmethod on the line above the def.
    def verify(self, value):
        """Return True if value passes this challenge. Each subclass decides how."""
        ...

    # TODO: make pretty_title an abstract PROPERTY. Use two decorators:
    #           @property          <- on top
    #           @abstractmethod    <- directly above the def
    def pretty_title(self):
        """Return the display title. Each subclass decides the format."""
        ...


# Step 2: a blog challenge. It is complete when a pull request number is merged.
# The constructor first calls the parent constructor:
#     super().__init__(number, title)
# and then stores its own extra argument.
#
#     challenge = BlogChallenge(7, 'Classes', [12, 18])
#     challenge.number        -> 7
#     challenge.title         -> 'Classes'
#     challenge.merged_prs    -> [12, 18]
#     challenge.pretty_title  -> 'PCC7 - Classes'     (no parentheses: a property)
#     challenge.verify(18)    -> True                 (18 is in merged_prs)
#     challenge.verify(20)    -> False
class BlogChallenge(Challenge):

    def __init__(self, number, title, merged_prs):
        # TODO: call the parent constructor (see the comment above the class).
        # TODO: store merged_prs as self.merged_prs.
        ...

    def verify(self, merged_pr):
        """Return True if merged_pr is in self.merged_prs, else False."""
        ...

    @property
    def pretty_title(self):
        """Return 'PCC<number> - <title>', for example 'PCC7 - Classes'."""
        ...


# Step 3: a bite challenge. It is complete when an answer equals the expected
# result. Same pattern as Step 2: call the parent constructor, then store result.
#
#     challenge = BiteChallenge(4, 'Add', 7)
#     challenge.result        -> 7
#     challenge.pretty_title  -> 'Bite 4. Add'
#     challenge.verify(7)     -> True                 (7 == result)
#     challenge.verify(8)     -> False
class BiteChallenge(Challenge):

    def __init__(self, number, title, result):
        # TODO: call the parent constructor, then store result as self.result.
        ...

    def verify(self, result):
        """Return True if result == self.result, else False."""
        ...

    @property
    def pretty_title(self):
        """Return 'Bite <number>. <title>', for example 'Bite 4. Add'."""
        ...
''',
    "tests": '''import inspect

import pytest

from challenge import BiteChallenge, BlogChallenge, Challenge


@pytest.fixture
def blog_challenge():
    merged_prs = [41, 42, 44]
    return BlogChallenge(1, 'Wordvalues', merged_prs)


@pytest.fixture
def bite_challenge():
    result = 'your function return value'
    return BiteChallenge(24, 'ABC and class inheritance', result)


def test_base_class_is_abstract():
    with pytest.raises(TypeError):
        Challenge(1, 'title')
    assert inspect.isabstract(Challenge)


def test_subclass_must_implement_the_api():
    class Incomplete(Challenge):
        def verify(self, value):
            return True
    with pytest.raises(TypeError):
        Incomplete(1, 'title')

    class NoVerify(Challenge):
        @property
        def pretty_title(self):
            return 'x'
    with pytest.raises(TypeError):
        NoVerify(1, 'title')


def test_blog_challenge(blog_challenge):
    assert blog_challenge.number == 1
    assert blog_challenge.title == 'Wordvalues'
    assert blog_challenge.merged_prs == [41, 42, 44]
    assert blog_challenge.pretty_title == 'PCC1 - Wordvalues'
    assert blog_challenge.verify(42)
    assert not blog_challenge.verify(43)


def test_bite_challenge(bite_challenge):
    assert bite_challenge.number == 24
    assert bite_challenge.title == 'ABC and class inheritance'
    assert bite_challenge.result == 'your function return value'
    assert bite_challenge.pretty_title == 'Bite 24. ABC and class inheritance'
    assert bite_challenge.verify('your function return value')
    assert not bite_challenge.verify('something else')


def test_pretty_title_is_a_property():
    assert isinstance(BlogChallenge.__dict__['pretty_title'], property)
    assert isinstance(BiteChallenge.__dict__['pretty_title'], property)


@pytest.mark.parametrize("cls", [BlogChallenge, BiteChallenge])
def test_subclasses_call_parent_constructor(cls):
    assert issubclass(cls, Challenge)
    assert 'super()' in inspect.getsource(cls.__init__)


def test_empty_merged_prs():
    challenge = BlogChallenge(0, '', [])
    assert challenge.pretty_title == 'PCC0 - '
    assert challenge.verify(0) is False


@pytest.mark.parametrize('result, other', [(0, 1), ('', 'x'), (None, ''), ([], [1]), ({}, {'a': 1})])
def test_falsy_and_unhashable_results(result, other):
    challenge = BiteChallenge(-1, '', result)
    assert challenge.verify(result) is True
    assert challenge.verify(other) is False
    assert challenge.pretty_title == 'Bite -1. '


def test_pretty_titles_use_current_attributes():
    blog = BlogChallenge(1, 'old', [0, 0, 8])
    bite = BiteChallenge(2, 'old', ['a'])
    blog.number, blog.title = 3, '  NEW title'
    bite.number, bite.title = 4, '  NEW title'
    assert blog.pretty_title == 'PCC3 -   NEW title'
    assert bite.pretty_title == 'Bite 4.   NEW title'
    assert blog.verify(0) is True
    assert blog.verify(9) is False
    assert bite.verify(['a']) is True
''',
    "mutations": [
        {"name": 'truthy_results_only', "old": 'return result == self.result', "new": 'return bool(result) and result == self.result'},
        {"name": 'result_identity', "old": 'return result == self.result', "new": 'return result is self.result'},
        {"name": 'first_pr_only', "old": 'return merged_pr in self.merged_prs', "new": 'return bool(self.merged_prs) and merged_pr == self.merged_prs[0]'},
        {"name": 'abstract_api_not_enforced', "old": '    @abstractmethod\n    def verify(self, value):', "new": '    def verify(self, value):'},
    ],
    "reference": '''from abc import ABC, abstractmethod


class Challenge(ABC):

    def __init__(self, number, title):
        self.number = number
        self.title = title

    @abstractmethod
    def verify(self, value):
        pass

    @property
    @abstractmethod
    def pretty_title(self):
        pass


class BlogChallenge(Challenge):

    def __init__(self, number, title, merged_prs):
        super().__init__(number, title)
        self.merged_prs = merged_prs

    def verify(self, merged_pr):
        return merged_pr in self.merged_prs

    @property
    def pretty_title(self):
        return f'PCC{self.number} - {self.title}'


class BiteChallenge(Challenge):

    def __init__(self, number, title, result):
        super().__init__(number, title)
        self.result = result

    def verify(self, result):
        return result == self.result

    @property
    def pretty_title(self):
        return f'Bite {self.number}. {self.title}'
''',
}

SPEC["hints"] = [
    'Concept: Python raises TypeError when you call a class that still has an @abstractmethod member. '
    'Challenge has two abstract members, so a subclass must override both verify and pretty_title.',
    'For an abstract property, stack the decorators in this order: @property on top, @abstractmethod '
    'directly above the def. The body of an abstract member can be just `pass`.',
    'In each subclass constructor, call super().__init__(number, title) first. It runs the Challenge '
    'constructor, which stores number and title. Then store the extra argument, for example '
    'self.merged_prs = merged_prs.',
]
