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

**Constraints:**

- Numbers are finite integers or floats; `bool` values are invalid.
