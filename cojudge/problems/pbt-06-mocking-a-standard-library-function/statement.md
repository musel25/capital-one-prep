In this Bite you will mock out a function of the standard library, more specifically random.sample. We wrote a small generator that produces hex colors. We also provided a fixture to initialize the generator so you can just call next(gen) to get the next hex value. Use unittest.mock's patch to mock out the call to sample. It might be a bit tricky, but once you get this one down you possess a valuable testing skill!

Have fun and keep calm and test with pytest!

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `colors`. The judge supplies it automatically.

```python
from random import sample

HEX = '0123456789ABCDEF'

def gen_hex_color():
    while True:
        yield '#' + ''.join(sample(HEX, 6))
```
