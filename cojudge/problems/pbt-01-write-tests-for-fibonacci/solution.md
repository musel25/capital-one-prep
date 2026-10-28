## Reference tests

```python
import pytest
from fibonacci import fib

@pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (3, 2), (10, 55), (50, 12586269025)])
def test_values(n, expected):
    assert fib(n) == expected

@pytest.mark.parametrize('n', [-1, -10])
def test_negative(n):
    with pytest.raises(ValueError):
        fib(n)
```
