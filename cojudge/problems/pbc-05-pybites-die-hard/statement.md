Given a listing of files for our *community* branch, determine:

 - Who opened the most pull requests (excluding PyBites)?

 - Which challenge has the most pull requests?

Complete the functions `gen_files` and `diehard_pybites` below.

The `docstring` for each function contains more information to help you solve the problem.

Here is an example of how it should work:

```python
>>> from urllib.request import urlretrieve
>>> from pcc_stats import diehard_pybites, gen_files
>>> urlretrieve('https://bites-data.s3.us-east-2.amazonaws.com/dirnames.txt', 'tempfile.txt')
('tempfile.txt', <http.client.HTTPMessage object at 0x7fc244708110>)
>>> ret = gen_files(tempfile='tempfile.txt')
>>> type(ret)
<class 'generator'>
>>> list(ret)
['03/mridubhatnagar', '03/aleksandarknezevic', '04/blair_young', '04/data', '32/bbelderbos', ...]
>>> diehard_pybites()
Stats(user='clamytoe', challenge=('01', 7))
>>> diehard_pybites(
...         files=[
...             "22/wonderfulboyx",
...             "25/bbelderbos",  # ignored
...             "25/clamytoe",
...             "21/wonderfulboyx",
...             "25/santiagobenitez",
...             "23/santiagobenitez",
...             "07/santiagobenitez"])
Stats(user='santiagobenitez', challenge=('25', 2))
```

**Constraints:**

- Paths use the form `NN/user`. Exclude `bbelderbos`, `juliansequeira`, and `pybites` from both counts. Ties keep first appearance order.
