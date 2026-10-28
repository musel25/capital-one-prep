# Pybites Pytest Path on CoJudge

[Open the course](https://cojudge.musel.dev/?course=pybites-pytest).

The ten exercises follow the [Pybites Pytest learning path](https://pybitesplatform.com/bites/paths/pytest/) in its original order.

1. Write tests for fibonacci
2. Write tests for list_to_decimal
3. Test print / standard output
4. Test fizzbuzz
5. Test code that parses json and ip ranges
6. Mocking a standard library function
7. Write tests for an account class
8. Zodiacal data parsing
9. Test a number guessing game
10. Test a movie db class

## Source and differences

`source-pages.json` records the public descriptions and visible editor content. Exercise 1 uses the original visible Fibonacci code. The original code and templates for exercises 2–10 were not available to this account. Those exercises are labeled offline recreations. Their statements define the complete local API. The zodiac data is constructed practice data.

Learners write tests. A submission must pass against correct code, cover at least 90% of its executable statements, and detect all supplied faulty variants. The course has 57 faults across 67 judge checks. Reference tests appear under **Reference Solution**.

The runner uses the OOP course's small pytest subset. It supports parametrization, raises with match, function and yield fixtures, numeric approx, fail, Python stream capture, monkeypatch setattr/setitem, tmp_path, and unittest.mock.patch. It distinguishes a fixture that returns a generator from a yield fixture. Fixture values are shared within one test and recreated for the next test. Teardown runs after failures.

The runner measures statement coverage with Python tracing. It does not run pytest-cov or mutatest. Advanced pytest features and plugins are outside this course's contract. Like the OOP course, the supplied grader is included in the editable file. Keep that section unchanged.

## Files and verification

- `specs.py`: supplied modules, contracts, reference tests, and explicit faults.
- `runner.py`: standalone test-writing judge, built from the existing OOP helpers.
- `support.py`: course generator and local verifier.
- `../../scripts/pytest_path.py`: build, verify, and live verification commands.
- Output: `../problems/pbt-*` and `../courses/pybites-pytest`.

Run from the repository root:

```sh
uv run python scripts/pytest_path.py verify
uv run pytest tests/test_pytest_path.py -q
uv run python scripts/pytest_path.py build
```

Verify the deployed judge through an SSH tunnel:

```sh
ssh -N -L 15429:127.0.0.1:5379 my-vps
uv run python scripts/pytest_path.py live --base-url http://127.0.0.1:15429
```

Publish only `cojudge/problems/pbt-*` and `cojudge/courses/pybites-pytest` to the existing content volume. No application rebuild is required. Do not replace other content or progress files. The CLI checks reference and starter code through `/api/submit`; it does not mark problems complete or save learner solutions.

## Publication check — October 28, 2026

Published the new problem and course directories to the existing `cojudge-trial-data` volume. The application image and other courses were unchanged. The browser displayed all ten titles in the source order. All ten reference submissions were accepted by the deployed Docker judge. All ten starter submissions were rejected. No learner solution or completion flag was saved by these API checks.

Local checks: all 9 runner regression tests passed. All ten references passed under real pytest as well. The CLI generated all ten starter files correctly. A full repository run passed 106 tests before the last two regression tests and concurrent course work appeared. A later run had 109 passing tests and 24 failures from missing builders in the unfinished `tests/test_data_formats_course.py` and `tests/test_sqlmodel_course.py` work. Another full run stopped during collection while `tests/test_datetimes_course.py` lacked its module. These files belong to other work and were not changed for this course.
