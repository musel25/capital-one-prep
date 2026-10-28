# 03. Pickling objects

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/pickling-objects/)

Implement `deserialize(file=None)` and `serialize(file, data=None)`. Paths can be strings or pathlib Paths. Read and write files in binary mode using pickle. `deserialize(path)` returns the stored object unchanged, including namedtuple types. With no path, deserialize the trusted local `DEFAULT_PICKLE` bytes into a list of `Record(name, score)` values. `serialize` writes the supplied data and returns `None`. Only when `data is None`, call `deserialize()` for default data. Empty lists and other false values must be stored as supplied. Replace existing file content. Missing files raise `FileNotFoundError`; invalid pickle data raises `pickle.UnpicklingError` or `EOFError`. Only load trusted exercise data.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium template and tests are recreated. Trusted pickle bytes built from a small local namedtuple list replace the downloaded default file. `deserialize(None)` selects that local default; explicit paths still use files.

<details>
<summary>Original public description</summary>

In this Bite you will load (deserialize) and dump (serialize) a data structure from / to a `pickle` file which support storing your own objects, interesting!

*As compared to JSON pickle is a binary serialization format, so it's not human-readable. It can represent an extremely large number of Python types. On the flip side though, deserializing untrusted JSON does not in itself create an arbitrary code execution vulnerability, pickle does which makes it unsecure.*

Complete the two following functions to (un)pickle data:

 1. `deserialize`: loads in the passed in `pickle` file path and returns the data structure it retrieves from it (a `list` of `namedtuple`s).

2. `serialize`: takes a `pickle` file path to pickle the data to. It's either the data passed in (second argument) or, if no data is provided (`data is None`), it calls `deserialize` to get the default data (again a `list` of `namedtuple`s).

We hope this Bite gets you up2speed with serializing data using the `pickle` module.

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`pickling`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
