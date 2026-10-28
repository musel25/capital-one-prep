# 12. Alternative constructors

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/alternative-constructors/)

**Inputs and required behavior for this version:**

All inputs are strings. Direct domain names contain no whitespace. Use the template's simplified rule r'.*\.[a-z]{2,3}$'; this is not full DNS validation. An empty name or a name that fails this rule raises DomainException. Keep accepted names unchanged. URLs use http or https, with a host and optional numeric port, path, query, or fragment. Validate the full network location, including its port if present; a numeric port therefore fails the domain rule. Credentials and malformed URLs are excluded. Emails have exactly one @ and a nonempty local part and domain part. Other email forms are excluded. Both classmethods extract the domain and use the same validation. Return an instance of the calling class. str(domain) returns its name. Other input types are excluded.

<details>
<summary>Original bite description</summary>

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

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `constructors`. **Run** checks the first three tests. **Submit** runs all
26. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
