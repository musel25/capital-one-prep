## Reference solution

Use this implementation above the supplied tests and runner.

```python
def cached_property(func):
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
```
