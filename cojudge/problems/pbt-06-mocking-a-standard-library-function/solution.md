## Reference tests

```python
from unittest.mock import patch
import pytest
from colors import gen_hex_color, HEX

@pytest.fixture
def gen():
    return gen_hex_color()

def test_colors(gen):
    with patch('colors.sample', side_effect=[list('A1B2C3'), list('FEDCBA')]) as sample:
        assert next(gen) == '#A1B2C3'
        assert next(gen) == '#FEDCBA'
        assert sample.call_count == 2
        sample.assert_called_with('0123456789ABCDEF', 6)
```
