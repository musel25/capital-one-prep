You know the index at the end of a book where you look up which pages people and terms occur? Useful right?

In this Bite you will build your own, but instead of page numbers we will use line numbers.

We will be using the story of [Little Red Riding Hood](https://www.dltk-teach.com/rhymes/littlered/story.htm) (the tests also run your code against [The Needle Tree](https://parenting.firstcry.com/articles/top-15-short-moral-stories-for-kids/)).

Complete `make_character_index` (scroll down) that takes a multiline text (story) string and a list of characters.

Parse the text and match the characters (case insensitively) keeping track of the line numbers where they appeared.

One twist: some characters have synonyms, in that case you have to match them all and return the first one, e.g. when one of `('Grandmother', 'Grandma', 'Granny')` matches, you return the first = *Grandmother*.

The return data is a `dict` where the *keys* are the characters and the *values* are `list`s of line numbers of (unique) appearances in **sorted** order.

See also the *tests* for the expected data.

We hope this is a fun exercise that keeps your Python fresh. Now go crack this Bite and remember: keep calm and code in Python!

**Constraints:**

- Aliases are nonempty and have word characters at both ends. Match whole words and count blank physical lines.
