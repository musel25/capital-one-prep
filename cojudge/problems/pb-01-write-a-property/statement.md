# 01. Write a property

[Course list](/?course=pybites-oop) · Pybites Beginner · [Original bite](https://pybitesplatform.com/bites/write-a-property/)

**Inputs and required behavior for this version:**

name is a string, including an empty string. expires is a naive datetime. Store both values. The read-only expired property returns a bool on each access: expires < the module's NOW. Equality is not expired. Changes to expires take effect on the next access. Other input types and timezone-aware datetimes are outside the contract; no validation is required for them.

<details>
<summary>Original bite description</summary>

Write a simple `Promo` class. Its constructor receives two variables: `name` (which must be a string) and `expires` (which must be a `datetime` object).

Add a [`property`](https://docs.python.org/3/library/functions.html#property) called `expired` which returns a boolean value indicating whether the promo has expired or not.

Checkout the tests and `datetime` module for more info. Have fun!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `simple_property`. **Run** checks the first three tests. **Submit** runs all
8. A failing test shows its name, the error, and the failed test line. The template and tests are the originals from this free bite.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
