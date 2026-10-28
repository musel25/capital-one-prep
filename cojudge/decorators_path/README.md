# Pybites Decorators and Context Managers Path

[Open the course](https://cojudge.musel.dev/?course=pybites-decorators-context-managers).
[Original learning path](https://pybitesplatform.com/bites/paths/decorators-context/).

The twelve exercises follow the source order. Select Python.

Exercise 7 retains the original free Account template and tests, plus the
boundary checks used by the existing OOP course. This account does not expose
the premium templates or tests for the other eleven exercises. Those templates
and tests are recreated from the public descriptions. Each problem states its
complete local API and input guarantees. Source links and adaptation notes
appear in Course help.

The course uses the existing Python 3.11 Pybites runner and the standard library.
Tests use controlled clocks and call counters. They do not wait for real time,
fetch data, or use random outcomes. Some local choices make underspecified
source behavior explicit: set ordering for countdowns, read-only cache deletion,
three total retry attempts, and alert behavior after the daily threshold.

Learners write code above the supplied tests and runner. Keep those sections
unchanged. The tests are visible in the editor, as in the other Pybites courses.
The judge checks behavior; it cannot prove `contextlib.suppress` was used.
It does check the callable dispatch interface in the singledispatch exercise.

## Files

- `source-pages.json`: source order, URLs, levels, access notes, and the available
  free Account template and tests, retrieved on October 28, 2026.
- `bites/b01.py` through `b12.py`: tasks, templates, references, tests, and faults.
- `support.py`: native problem generation and local verification.
- `../../scripts/decorators_path.py`: build, verify, and live checks.
- Generated content: `../problems/pbdc-*` and
  `../courses/pybites-decorators-context-managers`.

## Verification

From the repository root:

```sh
uv run pytest -q tests/test_decorators_course.py
uv run python scripts/decorators_path.py verify
uv run python scripts/decorators_path.py build
```

The verifier requires all 200 reference checks to pass, every starter to fail,
and all 60 prepared faults to fail. The course tests also run all reference
checks under real pytest, separately from the embedded runner.

Use an authorized SSH tunnel for deployed-judge checks:

```sh
ssh -N -L 15437:127.0.0.1:5379 my-vps
uv run python scripts/decorators_path.py live --base-url http://127.0.0.1:15437 --faults
```

Publish only the new `pbdc-*` problem directories first. Keep the course index
unpublished until the judge checks pass. Publish the course index last. Its ID
matches the Foundation step already present in the home-page Learning path.
No application restart is required. Live API checks do not save learner code
or completion flags. Keep instructor verification artifacts outside learner
attempt folders and the served content directory.
