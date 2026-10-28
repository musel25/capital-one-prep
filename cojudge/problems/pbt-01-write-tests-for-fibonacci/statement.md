Our first Test Bite! The concept is simple: to pass a Test Bite, you write tests for the program under the "Code to Test" tab. We run pytest-cov and mutatest against your code to see if your tests are strong enough. To kick this off we have you write some tests for fib which generates a Fibonacci sequence. Note that we use the functool.cache decorator so we can also test higher numbers without timing out.

Good luck and keep calm and code in Python! 🐍 💪

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `fibonacci`. The judge supplies it automatically.

```python
from functools import cache

@cache
def fib(n):
   if n < 0:
        raise ValueError
   elif n in (0, 1):
       return n
   else:
       return(fib(n-1) + fib(n-2))
```
