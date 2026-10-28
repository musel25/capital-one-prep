In this Bite you will load (deserialize) and dump (serialize) a data structure from / to a `pickle` file which support storing your own objects, interesting!

*As compared to JSON pickle is a binary serialization format, so it's not human-readable. It can represent an extremely large number of Python types. On the flip side though, deserializing untrusted JSON does not in itself create an arbitrary code execution vulnerability, pickle does which makes it unsecure.*

Complete the two following functions to (un)pickle data:

 1. `deserialize`: loads in the passed in `pickle` file path and returns the data structure it retrieves from it (a `list` of `namedtuple`s).

2. `serialize`: takes a `pickle` file path to pickle the data to. It's either the data passed in (second argument) or, if no data is provided (`data is None`), it calls `deserialize` to get the default data (again a `list` of `namedtuple`s).

We hope this Bite gets you up2speed with serializing data using the `pickle` module.

Trusted local pickle bytes replace the downloaded default file.

**Constraints:**

- Paths are strings or `Path` objects; `deserialize()` uses the trusted local default.
- Only `data is None` selects default data; serialization returns `None` and replaces file contents.
