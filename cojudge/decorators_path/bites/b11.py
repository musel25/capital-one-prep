"""Recreated cached property exercise; no premium source code used."""

SPEC = {
    "title": "Cached property decorator",
    "module": "cached",
    "contract": "cached_property(func) returns a read-only cached descriptor or property. Compute once per "
                "instance after the first successful access. Cache every result, including None, False, 0, "
                "and empty values. Setting and deleting the property raise AttributeError, both before "
                "and after access. Failed computation is not cached; the next access retries. Different "
                "properties have separate caches. Preserve the function's docstring on the descriptor. "
                "Instances have a writable __dict__. Direct __dict__ tampering and slot-only objects are "
                "outside this exercise. Keep the supplied Planet(name, mass_value) class: its mass property "
                "uses cached_property and calls its _compute_mass() method. Use no sleep, network, or random data.",
    "statement": """Implement `cached_property` in `cached`.

The first successful access computes and stores the value for that instance.
Later accesses return the stored value, including false or empty values. A
failed computation must allow another attempt. Keep separate caches for each
instance and each property. Preserve the decorated method's docstring.

This local API is read-only: assignment and deletion must raise `AttributeError`
before and after the first access. Direct changes to `__dict__` and objects
without `__dict__` are outside the exercise.

The supplied `Planet` class represents an expensive mass calculation without
waiting or external data. After `earth = Planet('Earth', 5.97)`, repeated reads
of `earth.mass` return `5.97` and call `earth._compute_mass()` only once.
""",
    "template": '''def cached_property(func):
    """Return a read-only property that caches successful results."""
    return property(func)


class Planet:
    def __init__(self, name, mass_value):
        self.name = name
        self._mass_value = mass_value

    def _compute_mass(self):
        # Stand-in for an expensive calculation. Do not add a delay.
        return self._mass_value

    @cached_property
    def mass(self):
        """The mass value computed for this planet."""
        return self._compute_mass()
''',
    "tests": '''import pytest

from cached import Planet, cached_property


@pytest.mark.parametrize('value', [None, False, 0, '', (), [], {}, 7])
def test_all_results_are_cached(value):
    class Sample:
        calls = 0
        @cached_property
        def result(self):
            self.calls += 1
            return value
    sample = Sample()
    assert sample.result is value
    assert sample.result is value
    assert sample.calls == 1


def test_instances_do_not_share_cache():
    class Sample:
        def __init__(self, value):
            self.value = value
            self.calls = 0
        @cached_property
        def result(self):
            self.calls += 1
            return self.value
    first, second = Sample('first'), Sample('second')
    assert first.result == 'first'
    assert second.result == 'second'
    first.value = 'changed'
    assert first.result == 'first'
    assert first.calls == second.calls == 1


def test_different_properties_have_separate_cache():
    class Sample:
        calls = []
        @cached_property
        def first(self):
            self.calls.append('first')
            return 1
        @cached_property
        def second(self):
            self.calls.append('second')
            return 2
    sample = Sample()
    assert (sample.first, sample.second, sample.second, sample.first) == (1, 2, 2, 1)
    assert sample.calls == ['first', 'second']


@pytest.mark.parametrize('access_first', [False, True])
def test_assignment_is_rejected_before_and_after_access(access_first):
    class Sample:
        @cached_property
        def value(self):
            return 4
    sample = Sample()
    if access_first:
        assert sample.value == 4
    with pytest.raises(AttributeError):
        sample.value = 99
    assert sample.value == 4


@pytest.mark.parametrize('access_first', [False, True])
def test_deletion_is_rejected_before_and_after_access(access_first):
    class Sample:
        @cached_property
        def value(self):
            return 4
    sample = Sample()
    if access_first:
        assert sample.value == 4
    with pytest.raises(AttributeError):
        del sample.value
    assert sample.value == 4


def test_failed_computation_retries_and_then_caches():
    failure = ValueError('not ready')
    class Sample:
        calls = 0
        @cached_property
        def value(self):
            self.calls += 1
            if self.calls == 1:
                raise failure
            return 9
    sample = Sample()
    with pytest.raises(ValueError) as caught:
        sample.value
    assert caught.value is failure
    assert sample.value == 9
    assert sample.value == 9
    assert sample.calls == 2


def test_descriptor_preserves_docstring():
    class Sample:
        @cached_property
        def value(self):
            """A documented cached result."""
            return 1
    assert Sample.value.__doc__ == 'A documented cached result.'


def test_cached_mutable_result_keeps_identity():
    class Sample:
        @cached_property
        def value(self):
            return []
    sample = Sample()
    stored = sample.value
    stored.append('item')
    assert sample.value is stored
    assert sample.value == ['item']


def test_planet_uses_compute_method_once():
    class CountingPlanet(Planet):
        calls = 0
        def _compute_mass(self):
            self.calls += 1
            return super()._compute_mass()
    earth = CountingPlanet('Earth', 5.97)
    assert earth.name == 'Earth'
    assert earth.mass == 5.97
    earth._mass_value = 8
    assert earth.mass == 5.97
    assert earth.calls == 1
    assert Planet('Mars', 0.642).mass == 0.642
''',
    "reference": '''def cached_property(func):
    cache_key = object()
    def getter(instance):
        if cache_key not in instance.__dict__:
            instance.__dict__[cache_key] = func(instance)
        return instance.__dict__[cache_key]
    return property(getter, doc=func.__doc__)


class Planet:
    def __init__(self, name, mass_value):
        self.name = name
        self._mass_value = mass_value

    def _compute_mass(self):
        return self._mass_value

    @cached_property
    def mass(self):
        """The mass value computed for this planet."""
        return self._compute_mass()
''',
    "mutations": [
        {"name": "falsy_results_recomputed", "old": "if cache_key not in instance.__dict__:", "new": "if not instance.__dict__.get(cache_key):"},
        {"name": "all_properties_share_key", "old": "cache_key = object()", "new": "cache_key = '_shared_cached_value'"},
        {"name": "allow_assignment", "old": "return property(getter, doc=func.__doc__)", "new": "return property(getter, lambda instance, value: instance.__dict__.__setitem__(cache_key, value), doc=func.__doc__)"},
        {"name": "allow_deletion", "old": "return property(getter, doc=func.__doc__)", "new": "return property(getter, fdel=lambda instance: instance.__dict__.pop(cache_key, None), doc=func.__doc__)"},
        {"name": "lose_docstring", "old": "doc=func.__doc__", "new": "doc=None"},
    ],
    "examples": [{"input": "earth = Planet('Earth', 5.97); earth.mass; earth.mass", "output": "5.97, 5.97", "explanation": "Both reads use one successful computation for this instance."}],
    "notes": "Recreated local API. This property rejects both assignment and deletion. Planet uses fixed local data, with no waiting.",
    "original": False,
}
