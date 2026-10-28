# 11. Multiple inheritance (__mro__)

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/multiple-inheritance-__mro/)

**Inputs and required behavior for this version:**

Construct all four classes without arguments. Father and Mother inherit from Person. Child inherits from Father, then Mother. Each instance has the exact string shown in the description. Father and Mother reuse the Person string through inheritance. Only Person contains the literal 'I am a person'. No instance inputs or additional validation are required.

<details>
<summary>Original bite description</summary>

Implement the following `class` structure: `print(Child.__mro__)`:

```python
(<class '__main__.Child'>,
 <class '__main__.Father'>,
 <class '__main__.Mother'>,
 <class '__main__.Person'>,
 <class 'object'>)

```

Each class has the following string representation:

```python
person = Person()
dad = Father()
mom = Mother()
child = Child()

print(person)
print(dad)
print(mom)
print(child)

```

Output:

```python
I am a person
I am a person and cool daddy
I am a person and awesome mom
I am the coolest kid

```

You should use inheritance here, so the *I am a person* substring should only occur in the `Person` base class.

Good luck and keep calm and code in Python!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `mro`. **Run** checks the first three tests. **Submit** runs all
11. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
