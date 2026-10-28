# 15. Abc's and class inheritance

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/abcs-and-class-inheritance/)

**Inputs and required behavior for this version:**

Challenge takes an int number and str title. Empty titles and zero or negative numbers are allowed. Do not normalize or validate them. Challenge is abstract; verify and the pretty_title property must both be implemented before a subclass can be instantiated. Subclass constructors call super(). BlogChallenge takes a list of int PR numbers, including an empty list; verify checks membership. BiteChallenge takes a result and verifies it with ==, including falsy or unhashable built-in values. pretty_title formats the current number and title as 'PCCN - TITLE' or 'Bite N. TITLE'. Other number, title, and PR container types are outside this exercise.

<details>
<summary>Original bite description</summary>

`ABC`'s or `Abstract Base Classes` are great to enforce a common *API* for your subclasses.

You define one or more methods and/or properties as abstract in the base class, and if the subclass does not implement them it raises a `TypeError`. In this bite you will use this concept as follows:

1. Define a Challenge base class that inherits from `ABC` (given), its constructor receives a `number` and a `title` attribute.
1. On Challenge define an `abstractmethod` called `verify` and a `property` (< 3.3 it would be an `abstractproperty`) called `pretty_title`.
1. Create the `BlogChallenge` and `BiteChallenge` classes which both inherit from `Challenge`. *Note that they would raise a `TypeError` at this point, exactly what you want: enforcing the use of the abstract method/ property.*
1. `BlogChallenge` and `BiteChallenge`'s constructors call the parent constructor (don't worry it's *super*cool, remember: **we use Python3** so adjust your syntax), and both receive an extra argument in the constructor: `merged_prs` for `BlogChallenge` and `result` for `BiteChallenge`.
1. Implement the required methods and properties, refer to the tests what they need to return.

Get coding, learn more about classes, and have fun!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `challenge`. **Run** checks the first three tests. **Submit** runs all
14. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
