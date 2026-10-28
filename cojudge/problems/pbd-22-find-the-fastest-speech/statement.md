# 22. Find the fastest speech

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/find-the-fastest-speech/)

get_srt_section_ids(text) parses blank-line-separated SRT blocks: integer ID, HH:MM:SS,mmm --> HH:MM:SS,mmm, and one or more caption lines. Join caption lines with one space; count all characters, including punctuation and internal spaces. Strip line edges. Rank by characters per second, descending. Preserve block order for equal rates. Return integer IDs. Empty input returns []. Reject invalid timestamps, duplicate IDs, and nonpositive duration with ValueError. Accept CRLF newlines.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

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

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`srt`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
