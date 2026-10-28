In this Bite you will parse an [SRT](https://en.wikipedia.org/wiki/SubRip) (SubRip Subtitle file / video captions or subtitles).

This is a snippet that shows how such a file is formatted:

```python
...
5
00:00:18,080 --> 00:00:22,180
Because if you're really new to Python, we really recommend to start with the Newbies,

6
00:00:22,180 --> 00:00:26,260
and otherwise gauge your level doing the 10 Introductory Bites.
...
```

Each block is separated by two newlines and consists of:
- a section number,
- a start and an end time, separated by `-->`,
- the actual caption or subtitle text.

Calculate the differences between start and end times for each section, returning a list of section ids ordered by the fastest speech (= most chars spoken per second).

Here is an example how the code should work:

```python
>>> text = """
... 1
... 00:00:00,498 --> 00:00:02,827
... Beautiful is better than ugly.
...
... 2
... 00:00:02,827 --> 00:00:06,383
... Explicit is better than implicit.
...
... 3
... 00:00:06,383 --> 00:00:09,427
... Simple is better than complex.
... """
>>> from srt import get_srt_section_ids
>>> get_srt_section_ids(text)
[1, 3, 2]
```

**Constraints:**

- Join caption lines with one space; count punctuation and spaces; preserve block order for equal rates.
- Empty input returns `[]`; invalid timestamps, duplicate IDs, or nonpositive durations raise `ValueError`.
