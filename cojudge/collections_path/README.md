# Pybites Collections Path

[Open the course](https://cojudge.musel.dev/?course=pybites-collections).
[Original learning path](https://pybitesplatform.com/bites/paths/collections/).

The 11 exercises keep the source path order. Select Python.

- Exercises 1 and 6 retain the original free templates and tests. Added tests check boundaries.
- Exercise 8 retains the original free tests and function signatures. The template supplies the original movie CSV offline. Its four required columns are compressed into the editor. No download is needed.
- The other eight exercises use recreated templates and tests based on the public descriptions. The account does not provide their premium code. Each problem states its exact input contract.
- Exercise 10 supplies the original 2018 holiday table. A small standard-library `BeautifulSoup` adapter supports the documented table operations. It is not the third-party package.
- The RSS, contribution, word, and dialogue examples are supplied local data. They do not claim to reproduce the full remote datasets.

`source-pages.json` stores the public descriptions and available free templates/tests, retrieved on October 28, 2026. `bites.py` stores the contracts, templates, tests, reference solutions, and deliberate faults. `fixtures.py` supplies compressed data and the HTML adapter. The movie CSV and holiday table came from:

- https://bites-data.s3.us-east-2.amazonaws.com/movie_metadata.csv
- https://bites-data.s3.us-east-2.amazonaws.com/us_holidays.html

The existing Pybites runner executes each test in Python 3.11. Every reference must pass. Every starter must fail at least one test. Each deliberate fault must fail a test. These checks validate the supplied tests, not protection against an editor that alters its own tests.

From the repository root:

```bash
uv run pytest tests/test_collections_course.py -q
uv run python scripts/collections_course.py verify
uv run python scripts/collections_course.py build
ssh -N -L 15379:127.0.0.1:5379 my-vps
uv run python scripts/collections_course.py live --base-url http://127.0.0.1:15379
```

Publish only `cojudge/problems/pbc-*` and `cojudge/courses/pybites-collections` into the matching directories under `/var/lib/docker/volumes/cojudge-trial-data/_data/`. Check that those paths do not already exist before the first publication. No application restart is required. The live checks submit code directly to the judge. They do not call the progress API or save learner files.

For CLI checks, set `COJUDGE_CONTENT_DIR` to this repository's `cojudge` folder. Extract the reference implementation from `solution.md` and keep the supplied tests and runner below it. Use `cojudge init`, `cojudge run`, and `cojudge submit` as described in the main Cojudge problem guide.

## Publication checks — October 28, 2026

All 11 exercises are published. The live judge accepted all 79 reference test cases and rejected all 11 unfinished templates. The 14 local course tests pass. CLI init produced all 11 exact templates. CLI run accepted the queue reference and rejected its starter. The browser displays all 11 titles in source order, with progress at `0 / 11`. No progress API requests were used for verification.
