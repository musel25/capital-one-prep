# 08. Oop fun at the zoo

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/oop-fun-at-the-zoo/)

**Inputs and required behavior for this version:**

name is a string without newline characters. Empty names and duplicate names are valid. Apply str.title without trimming whitespace. Each new Animal gets the next shared integer ID; the first ID is 10001. str returns '<ID>. <Name>'. The classmethod zoo returns all created animals in creation order, joined with newlines and no trailing newline. An empty zoo returns ''. Repeated calls to str or zoo do not create animals or change IDs. Subclasses, direct attribute changes and other input types are outside the contract; no validation is required for them.

<details>
<summary>Original bite description</summary>

Finish the `Animal` class below adding one or more class variables and a `classmethod` so that the following code:

```python
dog = Animal('dog')
cat = Animal('cat')
fish = Animal('fish')
lion = Animal('lion')
mouse = Animal('mouse')
print(Animal.zoo())

```

... produces the following output:

```python
10001. Dog
10002. Cat
10003. Fish
10004. Lion
10005. Mouse

```

Few things to note here:

- The sequencing starts at 10000,
- Each animal gets title cased,
- An individual animal should print the sequence+name string as well, so best to implement the `__str__` method on the class.

So making another animal at this point, the following should work:

```python
horse = Animal('horse')
assert str(horse) == "10006. Horse"

```

As usual this is what the `pytest` code tests when you submit your code.

Have fun and code more Python! Join our growing developer Circle community to learn together with other passionate Pythonistas ...

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `zoo`. **Run** checks the first three tests. **Submit** runs all
9. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
