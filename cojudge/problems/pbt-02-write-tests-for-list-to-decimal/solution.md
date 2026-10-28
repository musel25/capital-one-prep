## Reference tests

```python
import pytest
from digits import list_to_decimal

@pytest.mark.parametrize('digits, expected', [([], 0), ([0], 0), ([9], 9), ([0, 4, 2, 8], 428), ([1, 0, 2], 102)])
def test_decimal(digits, expected):
    assert list_to_decimal(digits) == expected

@pytest.mark.parametrize('digit', [True, False, 3.6, '4', None])
def test_types(digit):
    with pytest.raises(TypeError):
        list_to_decimal([1, digit])

@pytest.mark.parametrize('digit', [-1, 10, 12])
def test_range(digit):
    with pytest.raises(ValueError):
        list_to_decimal([digit])
```
