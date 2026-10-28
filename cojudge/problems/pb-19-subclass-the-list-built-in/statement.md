# 19. Subclass the list built-in

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/subclass-the-list-built-in/)

**Inputs and required behavior for this version:**

Construct an IntList from an iterable of finite int or float values, with bool excluded. append accepts one number or a list of numbers. + and += accept lists of numbers. These three operations raise TypeError for invalid elements and do not change the list on failure. + returns a new IntList; += preserves identity. mean and median are read-only properties and do not reorder the list. On an empty list they raise statistics.StatisticsError. Constructor validation, other mutation methods, nonfinite numbers, and non-list operands for + or += are outside this exercise.

<details>
<summary>Original bite description</summary>

In this Bite you will complete `IntList`, a subclass of `list`, which should be able to do the following:

```python
>>> from intlist import IntList
>>> mylist = IntList([1, 3, 5])
>>> mylist.mean
3
>>> mylist.median
3
>>> mylist.append(7)
>>> mylist.append(1.0)
>>> mylist.mean
3.4
>>> mylist.median
3
>>> mylist.append('a')
...
TypeError
>>> mylist.append([2, 3])
>>> mylist.append([2, 'a'])
...
TypeError
>>> mylist += [1]
>>> mylist += [1, 'a']
...
TypeError

```

As you see this *special* list is enriched with `mean` and `median` *properties*, and is restricted to `int` values only, be it as appended individually or as `list` of `int`s. Apart from overriding `append`, you'll also need to tweak the `__add__` and `__iadd__` (operator overloading) *[dunder methods](https://dbader.org/blog/python-dunder-methods)* here.

Enjoy and keep calm and code more Python!

</details>

**Notes for this version:** As in the description's REPL example, numbers such as `1.0` are accepted; other types raise `TypeError`.

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `intlist`. **Run** checks the first three tests. **Submit** runs all
15. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
