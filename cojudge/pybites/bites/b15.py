"""Bite: Abc's and class inheritance (recreated tests and template)."""

SPEC = {
    "title": "Abc's and class inheritance",
    "module": "challenge",
    "template": '''from abc import ABC, abstractmethod


class Challenge(ABC):
    pass


class BlogChallenge(Challenge):
    pass


class BiteChallenge(Challenge):
    pass
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
''',
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
