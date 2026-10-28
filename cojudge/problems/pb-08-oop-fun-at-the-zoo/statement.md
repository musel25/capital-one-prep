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

**Constraints:**

- Names have no newline characters.
