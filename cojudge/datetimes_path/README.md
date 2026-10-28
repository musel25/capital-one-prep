# Pybites Datetimes and Timezones Path

[Open the course](https://cojudge.musel.dev/?course=pybites-datetimes-timezones).
[Original path](https://pybitesplatform.com/bites/paths/datetimes-timezones/).

All 24 exercises keep the source order. Select Python.

Exercises 1 and 2 retain the original free templates and tests. Added tests
check boundaries and state. Exercise 2 reuses the verified property exercise
from the OOP path, with a separate problem ID. The other 22 exercises use
recreated templates and tests based on the public descriptions. Each statement
specifies its input rules, fixed defaults, error behavior, and offline changes.

`source-pages.json` records the public descriptions and free code retrieved on
October 28, 2026. `bites.py` holds the contracts, tests, references, and deliberate
faults. `support.py` builds native Cojudge problem files with the existing Pybites
runner. `scripts/datetimes_course.py` builds and verifies this course.

The course uses Python 3.11 and the standard library. It supplies short local
log, subtitle, and activity examples. Exercise 15 uses constructed composer and
opera fixtures. Functions that originally suggested dateutil use calendar and
datetime operations instead. The statements define the accepted date formats.
Exercise 5 accepts an optional date for deterministic boundary checks. Other
exercises use fixed time defaults when their contract specifies a constant.

Exercise 10 includes IANA timezone data, version 2026b. `timezones.b85` contains
compressed TZif records from `/usr/share/zoneinfo`, with aliases from `tzdata.zi`.
`fixtures.py` embeds this archive in the editor and supplies a `ZoneInfo` loader
that returns standard-library ZoneInfo objects. This supports DST and legacy
names such as `US/Arizona` even when the judge image has no timezone files.
The IANA timezone database is public domain: <https://www.iana.org/time-zones>.
Keep the supplied timezone support code when you implement the meeting function.

Every reference must pass all tests. Every starter must fail at least one test.
Every deliberate fault must fail a test. These checks validate the supplied test
suite. The editor keeps tests visible, as in the existing OOP course.

```bash
uv run pytest tests/test_datetimes_course.py -q
uv run python scripts/datetimes_course.py verify
uv run python scripts/datetimes_course.py build
ssh -N -L 15379:127.0.0.1:5379 my-vps
uv run python scripts/datetimes_course.py live --base-url http://127.0.0.1:15379
```

Publish only `cojudge/problems/pbd-*` and
`cojudge/courses/pybites-datetimes-timezones` to the matching directories under
`/var/lib/docker/volumes/cojudge-trial-data/_data/`. Check that the target paths
are absent before first publication. No application restart is required.
The live check submits references and starters without calling the progress API.
For CLI checks, set `COJUDGE_CONTENT_DIR` to this repository's `cojudge` folder.
Use `cojudge init`, `cojudge run`, and `cojudge submit` as described in the main
Cojudge guide. Keep the supplied tests and runner with the reference solution.
Use an isolated OS home directory for CLI submission checks, since the CLI marks
accepted problems as solved in its local progress file.
