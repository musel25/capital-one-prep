# Python OOP Path

[Open the course](https://cojudge.musel.dev/?course=python-oop).

22 original exercises on object-oriented Python, in five levels: classes and
properties, state and behavior, inheritance and composition, dunder methods and
built-ins, and three small projects. The topics follow a common OOP learning
path; the scenarios, texts, and tests are written for this course.

The learner writes classes. A supplied driver (`driver.py`) runs each test's
steps on them: create objects, read and set attributes, call methods, apply
operators, run `with` blocks, and check structure such as `property`,
`classmethod`, the MRO, or abstract classes.

## Files

- `specs/oNN.py`: lesson, task, starter, reference classes, Java checker model,
  12 hand-written cases, a seeded generator for 20 more, and planted bugs.
- `driver.py`: the Python test driver and the shared Java checker kit.
- `support.py`: builder and verifier. `steps.py`: short helpers for test steps.
- Output: `../problems/oop-*`, `../courses/python-oop`, `../instructor/oop-*`.

## Checks

From the repository root:

```bash
uv run python scripts/oop_course.py verify   # Python reference vs. hand-written answers,
                                             # planted bugs caught, starter fails,
                                             # Java Marker agrees on all 32 tests
uv run python scripts/oop_course.py build
uv run python scripts/oop_course.py live --base-url http://127.0.0.1:15379
```

`live` needs an SSH tunnel to the judge (`ssh -N -L 15379:127.0.0.1:5379 my-vps`).
It submits the reference (must pass all tests) and the starter (must fail).

Publish: copy `problems/oop-*` and `courses/python-oop` into
`/var/lib/docker/volumes/cojudge-trial-data/_data/` on the VPS (root-only; use
`sudo -n`). The app reads them per request, so no restart is needed.
