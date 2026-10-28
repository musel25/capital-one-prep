# 07. Find the most common word

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/find-the-most-common-word/)

Implement `get_most_common_word(text=TEXT, stopwords=STOPWORDS)`. Lowercase the text. Split on whitespace. Remove non-alphanumeric characters from each token, so `can't` becomes `cant`. Ignore empty tokens and stopwords, matched without case. Count digits as alphanumeric. Return `(word, frequency)`. Ties keep first appearance order. Return `(None, 0)` if no words remain. Do not change the stopword collection.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Write a function that returns the most common (non stop)word in [this Harry Potter text](https://bites-data.s3.us-east-2.amazonaws.com/harry.txt).

Make sure you convert to lowercase, strip out *non-alphanumeric* characters and [stopwords](https://bites-data.s3.us-east-2.amazonaws.com/stopwords.txt). Your function should return a *tuple* of (`most_common_word`, `frequency`).

The template code already loads the Harry Potter text and list of stopwords in.

Check the tests for more info - have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`common_word`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
