Our 4th test Bite. Michael made a calculator that will be able to accept a list of decimal digits and returns an integer where each int of the given list represents decimal place values from first element to last. He wrote the function in such a way that it only accepts positive digits in range(0, 10) and anything that is not raises a ValueError if its out of range, or a TypeError if its not an int type.

Some examples: [0, 4, 2, 8] => 428 [1, 2] => 12 [3] => 3 [6, 2, True] => raises TypeError [-3, 12] => raises ValueError [3.6, 4, 1] => raises TypeError ['4', 5, 3, 1] => raises TypeError

In this Bite you are tasked to write the tests for this function.

Good luck and keep calm and code in Python!

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `digits`. The judge supplies it automatically.

```python
def list_to_decimal(digits):
    result = 0
    for digit in digits:
        if type(digit) is not int:
            raise TypeError('digits must be integers')
        if not 0 <= digit <= 9:
            raise ValueError('digits must be in range 0..9')
        result = result * 10 + digit
    return result
```
