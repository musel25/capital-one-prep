# 04. Top 10 pybites tags

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/top-10-pybites-tags/)

Implement `get_top_tags(xml=XML, n=10)`. Count the text of each RSS `<category>` element with `Counter`. Return `Counter.most_common(n)`: a list of `(tag, count)` tuples. Strip surrounding whitespace. Ignore empty categories. Keep case. Ties keep the first appearance order. `n` is a nonnegative integer. The XML is well formed and has no namespaces.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you will find the top ten tags found in the [PyBites blog](https://pybit.es) XML feed (e.g. *Python, Flask, Django, learning*).

The tests for this Bite expect you to use `collections.Counter` and we loaded a [static copy of our XML feed](https://bites-data.s3.us-east-2.amazonaws.com/feed) so we can predictably test your code. The PyBites tags will need to be parsed from the XML tags within each (Hint: you don't *need* an XML parser for this task).

What are PyBites people most passionate about? Look at the tests and you'll know the answer. Then write your solution to make the tests pass.

Keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`tags`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
