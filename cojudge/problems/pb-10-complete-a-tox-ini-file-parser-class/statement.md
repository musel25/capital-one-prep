# 10. Complete a tox ini file parser class

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/complete-a-tox-ini-file-parser-class/)

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

**Notes for this version:** The tests write sample tox ini files to a temporary folder and pass the file path, as in the description's REPL example. The first sample has the same shape as the Django tox file in that example.

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `ini`. **Run** checks the first three tests. **Submit** runs all
5. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
