# 16. Matrix multiplication / @ operator

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/matrix-multiplication-operator/)

Since 3.5 Python has a binary operator to be used for matrix multiplication: `@`, see [PEP 465 -- A dedicated infix operator for matrix multiplication](http://legacy.python.org/dev/peps/pep-0465/).

The *@ sign* can now be used on types implementing the `__matmul__` *special/magic/dunder* method.

It is important to note that whilst this feature shipped in 3.5, none of the standard library builtin types have matrix multiplication implementations. So let's try to implement it on a custom type for this Bite.

Implement a simple class called `Matrix` that takes a list of lists in its constructor.

Implement the `__matmul__`, `__rmatmul__` (reversed) and `__imatmul__` (in place) *dunder* methods.

*Yes, using `numpy` a `np.dot(self, other)` would suffice, but the point is to get you thinking about implementing @ yourself!*

Here is a how matrix multiplication works:

```python
A = [[1, 2],  [3, 4]]
B = [[11, 12], [13, 14]]

```

Doing A @ B would do the following multiplications:

```python
[[1 * 11 + 2 * 13,   1 * 12 + 2 * 14],
[3 * 11 + 4 * 13,   3 * 12 + 4 * 14]]

```

See the tests for more info. Good luck!

> Special thanks to [Anthony Shaw](https://twitter.com/anthonypjshaw) for providing the idea and collaborating with us on this Bite!

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `matmul`. **Run** checks the first three tests. **Submit** runs all
8. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
