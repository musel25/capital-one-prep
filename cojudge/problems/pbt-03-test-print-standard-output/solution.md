## Reference tests

```python
import pytest
from printing import print_even_numbers

@pytest.mark.parametrize('numbers, expected', [([], ''), ([1, 3], ''), ([0, 1, 2, 3, 4], '0\n2\n4\n'), ([-4, -3, -2], '-4\n-2\n'), ([2, 2], '2\n2\n')])
def test_output(numbers, expected, capsys):
    assert print_even_numbers(numbers) is None
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ''
```
