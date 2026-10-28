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
