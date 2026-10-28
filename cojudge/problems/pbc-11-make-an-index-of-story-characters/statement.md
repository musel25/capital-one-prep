# 11. Make an index of story characters

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/make-an-index-of-story-characters/)

Implement `make_character_index(text, characters)`. `text` is a multiline string. Each character is a nonempty string or nonempty tuple of aliases. The first alias is the output key. Match all aliases without case, with whole-word boundaries. Punctuation around a name is allowed. A name inside a longer word does not match. Treat alias text literally. Return a dictionary of characters that appear, with sorted unique 1-based physical line numbers. Blank lines count. One line appears only once per character, even if several aliases match. Return an empty dictionary for empty text or characters. Canonical keys are unique. Alias endpoints are word characters. Keep input collections unchanged.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

You know the index at the end of a book where you look up which pages people and terms occur? Useful right?

In this Bite you will build your own, but instead of page numbers we will use line numbers.

We will be using the story of [Little Red Riding Hood](https://www.dltk-teach.com/rhymes/littlered/story.htm) (the tests also run your code against [The Needle Tree](https://parenting.firstcry.com/articles/top-15-short-moral-stories-for-kids/)).

Complete `make_character_index` (scroll down) that takes a multiline text (story) string and a list of characters.

Parse the text and match the characters (case insensitively) keeping track of the line numbers where they appeared.

One twist: some characters have synonyms, in that case you have to match them all and return the first one, e.g. when one of `('Grandmother', 'Grandma', 'Granny')` matches, you return the first = *Grandmother*.

The return data is a `dict` where the *keys* are the characters and the *values* are `list`s of line numbers of (unique) appearances in **sorted** order.

See also the *tests* for the expected data.

We hope this is a fun exercise that keeps your Python fresh. Now go crack this Bite and remember: keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`story_index`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
