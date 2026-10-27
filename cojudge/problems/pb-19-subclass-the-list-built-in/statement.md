# 19. Subclass the list built-in

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/subclass-the-list-built-in/)

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

**Notes for this version:** As in the description's REPL example, numbers such as `1.0` are accepted; other types raise `TypeError`.

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `intlist`. **Run** checks the first three tests. **Submit** runs all
7. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
