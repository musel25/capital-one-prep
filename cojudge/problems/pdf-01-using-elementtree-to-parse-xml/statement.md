# 01. Using elementtree to parse xml

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/using-elementtree-to-parse-xml/)

Implement `get_tree(xml=XML)`, `get_movies(tree)`, and `get_movie_longest_runtime(movies)`. Parse XML text into an ElementTree root `Element`. Return a list of dictionaries copied from every `<movie>` element in the tree, in document order. Movie data is in XML attributes. Runtime values are `N min` with nonnegative integers, or `N/A`. Return the whole movie dictionary with the largest numeric runtime. Ignore `N/A`. Ties keep the first movie. Return `None` if there is no numeric runtime. Do not change input dictionaries. Malformed XML raises `xml.etree.ElementTree.ParseError`.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium template and tests are recreated. The small Nolan XML example is constructed locally. The public description does not specify return types or empty-input behavior; this version defines them above.

<details>
<summary>Original public description</summary>

In this Bite you will use `ElementTree` to parse some [Nolan movies](http://www.imdb.com/name/nm0634240/) we extracted from [OMDb](https://www.omdbapi.com).

Luckily most APIs switched to *JSON*, but sometimes *XML* is all there is, so at least learn to parse some! Complete the `get_tree`, `get_movies` and `get_movie_longest_runtime` functions below. See the docstrings and tests for more info.

Have fun and remember:

> Keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`xml_movies`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
