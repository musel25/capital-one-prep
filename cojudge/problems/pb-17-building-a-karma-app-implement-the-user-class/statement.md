# 17. Building a karma app - implement the user class

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/building-a-karma-app-implement-the-user-class/)

**Inputs and required behavior for this version:**

User names are strings, including the empty string. Transactions contain a User giver and an integer points value, including zero and negative values. Adding a transaction updates and returns the receiving User. Points preserve transaction order. The points property returns a detached list; changing that list does not change the User. Karma is their sum. Fans count distinct giver names, including when two giver objects have the same name. Comparisons use karma only. The properties are read-only. Invalid types and comparisons with other types are outside this exercise; no validation is required.

<details>
<summary>Original bite description</summary>

This Bite is about implementing a `User` class that keeps track of *karma* points received (Bite idea came from [our karmabot](https://github.com/pybites/karmabot)).

As it is an *Advanced* Bite we have you look at the tests to figure out the implementation, but we will say that the class uses 3 *magic/special/dunder* methods and 3 *properties*.

Good luck and have fun!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `karma`. **Run** checks the first three tests. **Submit** runs all
13. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
