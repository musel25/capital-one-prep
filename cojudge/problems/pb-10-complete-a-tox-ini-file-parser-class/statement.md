*The INI file format is an informal standard for configuration files for some platforms or software.* ([Wikipedia](https://en.wikipedia.org/wiki/INI_file)).

In this Bite you will use `configparser` to parse a [tox](https://tox.readthedocs.io/en/latest/) *ini file*.

Complete the `ToxIniParser` class, completing the *stub properties* making the tests happy.

Eh *properties*? No worries, check out [our article](https://pybit.es/articles/property-decorator/) and [YouTube video](https://www.youtube.com/watch?v=8BbngXWouzo).

See the *TESTS* tab. There is a lot of ini file data, so scroll down to the actual tests ...

Additionally here is how it would work in the Python REPL using [a copy of Django's tox ini file](https://bites-data.s3.us-east-2.amazonaws.com/django-tox.ini) saved to my local /tmp folder:

```python
>>> from ini import ToxIniParser
  >>> tox = ToxIniParser('/tmp/django-tox.ini')
  >>> tox.number_of_sections
  7
  >>> tox.environments
  ['py3', 'flake8', 'docs', 'isort']
  >>> tox.base_python_versions
  ['python3']

```

Good luck and keep calm and code in Python!

**Constraints:**

- Files are valid INI files with a `[tox]` section. Interpreter values are single names; do not expand brace expressions.
