# 05. Pybites die hard

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/pybites-die-hard/)

Implement `gen_files(tempfile)` and `diehard_pybites(files=FILES)`. The first function is a generator that reads a local UTF-8 file, strips each line, skips blank lines, and yields `NN/user` paths. The listing contains only valid two-digit challenge paths. The second function accepts any iterable of paths. Exclude `bbelderbos`, `juliansequeira`, and `pybites` from both counts. Each remaining path counts once. Return `Stats(user, challenge)` where challenge is `(challenge_id, count)`. Ties keep first appearance order. With no eligible paths, return `Stats(None, (None, 0))`.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

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

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`pcc_stats`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
