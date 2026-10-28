# Pybites Data Formats Path

[Open the course](https://cojudge.musel.dev/?course=pybites-data-formats).
[Original learning path](https://pybitesplatform.com/bites/paths/data-formats/).

The course contains the 17 requested exercises in their original order. Select Python.

Exercises 4 and 6 retain the available original free tests, with added boundary tests. Exercise 4 retains its original template. Exercise 6 retains its function signatures and supplies the original movie CSV offline, compressed to its four required columns. Exercises 4, 6, and 8 use independent copies of the specifications already used for the Collections course. Their problem IDs and saved solutions are separate.

The remaining premium templates and tests are unavailable in this account. Those exercises use recreated templates and tests based on their public descriptions. Each statement defines the exact interface and the offline changes. Small supplied datasets are constructed examples unless a statement identifies an original dataset. They do not claim to reproduce remote datasets or the premium tests. API calls use a supplied local client. SQLite exercises use the real standard-library `sqlite3` module.

`source-pages.json` stores public descriptions and available free templates/tests retrieved on October 28, 2026. The specification files define input contracts, local data, starters, references, tests, and deliberate faults. `support.py` builds native Cojudge problems using the established Python 3.11 runner in `cojudge/pybites/runner.py`.

Every reference must pass every supplied test. Every starter must fail at least one test. Each deliberate fault must fail a test. These checks validate the supplied tests. The existing runner requires learners to keep its supplied tests and runner unchanged.

From the repository root:

```bash
uv run pytest tests/test_data_formats_course.py -q
uv run python scripts/data_formats_course.py verify
uv run python scripts/data_formats_course.py build
ssh -N -L 15380:127.0.0.1:5379 my-vps
uv run python scripts/data_formats_course.py live --base-url http://127.0.0.1:15380
```

Publish only `cojudge/problems/pdf-*` and `cojudge/courses/pybites-data-formats` into the matching directories under `/var/lib/docker/volumes/cojudge-trial-data/_data/`. Check that those paths do not already exist before the first publication. No application restart is required. Direct live judge checks do not call the progress API or save learner files.

For CLI checks, set `COJUDGE_CONTENT_DIR` to a disposable directory containing the generated course and problems. The CLI seeds bundled content into its content directory. Use `cojudge init <id> --lang python --output <new-file>` to check starter creation. Use the complete reference code with the supplied tests and runner for execution checks. Keep validation files outside learner attempt folders.
