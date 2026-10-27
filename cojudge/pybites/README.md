# Pybites OOP Path on CoJudge

[Open the course](https://cojudge.musel.dev/?course=pybites-oop).

The 22 bites of the [Pybites OOP learning path](https://pybitesplatform.com/bites/paths/oop/),
in the same order, as CoJudge problems.

- **Description:** the public bite description (`source-pages.json`, downloaded from the bite pages).
- **Template and tests:** bites 1 and 14 are free bites, so they use the original template and
  tests (plus a few added tests, marked as added). The other 20 have their template and tests in
  Pybites premium; here they are recreations that follow the description. Bite 21 is an offline
  version (no network or BeautifulSoup in the judge; a small `Soup` table parser is supplied).
- **How it runs:** the editor holds the template, the pytest tests, and a supplied runner
  (`runner.py`). For each judge test, the runner loads the editor as the module the tests import,
  runs the tests in file order up to that one, and returns `passed` or
  `FAILED <test> | <error> | test line N: <code>`. A small pytest stand-in supports `raises`,
  `mark.parametrize`, `fixture`, `approx`, `capsys`, `monkeypatch`, and `tmp_path`.

## Files

- `bites/bNN.py`: module name, template, tests, and a reference solution.
- `support.py`: builder and verifier. `runner.py`: the runner and the `Marker.java` checker.
- Output: `../problems/pb-*` and `../courses/pybites-oop`.

## Checks

From the repository root:

```bash
uv run python scripts/pybites_course.py verify   # Python 3.11: reference passes all tests,
                                                 # template fails at least one
uv run python scripts/pybites_course.py build
uv run python scripts/pybites_course.py live --base-url http://127.0.0.1:15379
```

`live` needs `ssh -N -L 15379:127.0.0.1:5379 my-vps`. Publish by copying `problems/pb-*` and
`courses/pybites-oop` into `/var/lib/docker/volumes/cojudge-trial-data/_data/` (use `sudo -n`).
