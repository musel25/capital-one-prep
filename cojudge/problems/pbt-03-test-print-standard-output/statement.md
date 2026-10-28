In this Bite you test a function that prints to stdout. Check out pytest's Capturing of the stdout/stderr output how to test this. You probably want to use the capsys / capfd fixture in your test code and you'll probably find a good use case for @pytest.mark.parametrize here too.

Have fun and keep calm and code in Python!

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `printing`. The judge supplies it automatically.

```python
def print_even_numbers(numbers):
    for number in numbers:
        if number % 2 == 0:
            print(number)
```
