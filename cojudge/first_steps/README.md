# Python First Steps

[Open the course](https://cojudge.musel.dev/?course=python-first-steps).

25 tiny exercises for a complete beginner, for example a 14-year-old who has
never programmed. Each exercise teaches one new idea with a short example.

| Exercises | Idea |
| --- | --- |
| 01–05 | `print()`, math, text pictures, commas in `print()` |
| 06–07 | variables |
| 08–12 | `input()` and `int()` |
| 13–17 | `if`, `else`, `==`, `%`, edges such as `>=` |
| 18–20 | `elif` |
| 21–23 | `and`, `or` |
| 24–25 | small projects: rock-paper-scissors and a quiz |

The order follows common beginner courses: Codecademy Learn Python 3,
the HackerRank Python introduction, and CodingBat Warmup. All exercise text and
tests are original.

## How the judge checks

The problems use CoJudge script mode (`"scriptMode": true`, CoJudge commits
`5bc43f0` and `624f69f`). The editor contains only the learner's program; there
is no class and no supplied test code. Each test gives the program its input on
stdin. The judge compares the printed text with an independent Java version in
`Marker.java`. Spaces at the end of a line do not count. The question text of
`input("...")` is not printed. Errors show the line number and the message.

## Files

- `exercises.py`: lessons, tasks, starters, Python references, Java versions,
  tests, hints, and prepared mistakes.
- `support.py`: verification and native problem generation.
- `../../scripts/first_steps_course.py`: `build`, `verify`, and `live`.
- Generated content: `../problems/pfs-*` and `../courses/python-first-steps`.

## Verification

From the repository root:

```sh
uv run pytest -q tests/test_first_steps_course.py
uv run python scripts/first_steps_course.py verify
uv run python scripts/first_steps_course.py build
```

`verify` runs every Python reference and the Java version on all 128 tests and
requires the same text. Every starter must fail at least one test. All 34
prepared mistakes must fail at least one test.

`live` submits the references, starters, and mistakes to a running judge. It
does not save learner code or completion flags:

```sh
ssh -N -L 15381:127.0.0.1:5379 my-vps
uv run python scripts/first_steps_course.py live --base-url http://127.0.0.1:15381
```

Publish the `pfs-*` problem folders first and the course index last. The judge
must run CoJudge `624f69f` or later.
