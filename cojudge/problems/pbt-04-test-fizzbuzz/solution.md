## Reference tests

```python
import pytest
from fizzbuzz import fizzbuzz

@pytest.mark.parametrize('n, expected', [(1, 1), (2, 2), (3, 'Fizz'), (6, 'Fizz'), (5, 'Buzz'), (10, 'Buzz'), (15, 'FizzBuzz'), (30, 'FizzBuzz'), (0, 'FizzBuzz'), (-3, 'Fizz'), (-5, 'Buzz'), (-15, 'FizzBuzz')])
def test_fizzbuzz(n, expected):
    assert fizzbuzz(n) == expected
```
