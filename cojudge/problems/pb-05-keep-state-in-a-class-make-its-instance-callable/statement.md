# 05. Keep state in a class + make its instance callable

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/keep-state-in-a-class-make-its-instance-callable/)

**Inputs and required behavior for this version:**

Each call receives one finite int or float score, excluding bool. Scores may be negative or zero. Return the largest score received by this instance, including the current call. The first score is the initial record. Equal scores leave the record unchanged. Instances keep independent records. Other types, NaN and infinities are outside the contract; no validation is required for them.

<details>
<summary>Original bite description</summary>

In this Bite you write a small class to keep track of the max score in a game. When called as a function it receives a new score and returns the max score. Note it should work with negative numbers as well.

This is how it should work:

```python
>>> from record import RecordScore

  >>> record = RecordScore()
  >>> print(record(10))
  10
  >>> print(record(9))
  10
  >>> print(record(11))  # new max
  11

  >>> record = RecordScore()
  >>> print(record(-5))
  -5
  >>> print(record(-10))
  -5
  >>> print(record(-2))  # new max
  -2

```

Use the `__call__` dunder ("special") method to make the `RecordScore` class callable.

Good luck and keep calm and code in Python!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `record`. **Run** checks the first three tests. **Submit** runs all
8. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
