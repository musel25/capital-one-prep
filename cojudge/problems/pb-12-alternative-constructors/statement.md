In this Bite your are provided with a `Domain` class and a `DomainException` custom exception class.

You will add some validation to the current constructor to check if a valid domain name is passed in.

Next you will add a `__str__` special method to represent the object (basically the name attribute) and you will write two `classmethod`s to construct domains:

 1. from a **URL**

2. from an **email**

Here you can see the code in action (also make sure you check out the tests):

```python
>>> from constructors import Domain
>>> str(Domain('google.com'))
'google.com'
>>> str(Domain.parse_url("http://pybit.es"))
'pybit.es'
>>> domain = Domain.parse_email("julian@pybit.es")
>>> type(domain)
<class 'constructors.Domain'>
>>> str(domain)
'pybit.es'
```

Good luck and keep calm and code more Python!

**Constraints:**

- Use the supplied domain validation rule. URLs use HTTP or HTTPS; emails have one `@` and nonempty parts.
