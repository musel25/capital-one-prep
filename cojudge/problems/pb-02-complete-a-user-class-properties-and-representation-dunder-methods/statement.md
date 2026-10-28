# 02. Complete a user class: properties and representation dunder methods

[Course list](/?course=pybites-oop) · Pybites Beginner · [Original bite](https://pybitesplatform.com/bites/complete-a-user-class-properties-and-representation-dunder-methods/)

**Inputs and required behavior for this version:**

first_name and last_name are non-empty strings of ASCII letters A-Z or a-z. Empty names, whitespace, punctuation, non-ASCII names and other types are outside the contract; no validation is required for them. get_full_name returns both title-cased names with one space. username lowercases the first letter of first_name followed by at most seven letters of last_name. Both properties use the current attributes. str returns 'Full Name (username)'. repr returns ClassName("first_name", "last_name") with the original case and the instance's class name. Each instance keeps its own names.

<details>
<summary>Original bite description</summary>

In this Bite you are presented with another class, `User` this time.

Like last Bite you are asked to complete it, see the `TODO`s in the code below:

1. Complete the `get_full_name` property (more on *properties* [here](https://pybit.es/articles/property-decorator/)) that prints first and last name separated by a space.
1. Complete the `username` property following its *docstring*.
1. Complete the special representation [*dunder methods*](https://dbader.org/blog/python-dunder-methods): `__str__` and `__repr__`. Look at the tests what they should return. Brace yourself for some bonus learning for a twist we added in `__repr__` (but as it's a Beginner Bite we give you a hint!)

Apart from [Ned's awesome answer on SO](https://stackoverflow.com/a/1438297), to give you an idea about the difference between `__str__` and `__repr__`, check out how `datetime` implements them:

```python
>>> from datetime import datetime
>>> dt = datetime.now()
>>> str(dt)
'2019-02-04 23:05:27.376407'
>>> repr(dt)
'datetime.datetime(2019, 2, 4, 23, 5, 27, 376407)'

```

Good luck and keep calm and code in Python!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `user`. **Run** checks the first three tests. **Submit** runs all
9. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
