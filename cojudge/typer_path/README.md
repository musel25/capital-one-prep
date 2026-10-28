# Pybites Typer Path on CoJudge

[Open the course](https://cojudge.musel.dev/?course=pybites-typer).

The seven exercises from the [Pybites Typer path](https://pybitesplatform.com/bites/paths/typer/),
in the source order. Select Python.

The templates, tests, and reference solutions are recreations based on the public
bite descriptions. Each problem states its exact contract. The original premium
templates and tests are not visible in this account. These files do not claim to
reproduce those hidden tests.

The judge uses real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4. Each problem includes
`python-libs.zip`. It contains pure-Python package sources, package metadata, and
upstream licenses. The CoJudge Python runner loads it when `pythonDependencies`
is true. No packages are installed or downloaded while a solution runs. The
playground and debugger do not load this problem archive.

`requirements.txt` records every bundled version. Rebuild the archive with:

```sh
uv run --no-project --python 3.11 --with-requirements cojudge/typer_path/requirements.txt python cojudge/typer_path/vendor.py
```

From the repository root:

```sh
uv run python scripts/typer_path.py verify
uv run python scripts/typer_path.py build
uv run pytest tests/test_typer_path.py -q
uv run python scripts/typer_path.py live --base-url http://127.0.0.1:15379
```

The local verifier uses Python 3.11 with `-S`. It loads libraries from the archive,
not from the authoring environment. All 61 reference tests pass. Each unfinished
starter fails at least one test. Seven explicit faults must each fail a test.
`verification.json` records the checks that detect each fault.

The supplied OOP test runner supports the pytest features these tests use. It is
not a complete pytest installation. The progress-bar test observes the iterable
passed to the real bar. Table tests inspect real Rich table content and rendered
output. Password tests check hidden input, confirmation, retry, and aborted input.
Click 8.1's test stream does not raise EOF at end-of-input. The abort test therefore
supplies a stream that raises `EOFError`, as terminal input does.

Publish only `cojudge/courses/pybites-typer` and `cojudge/problems/pbty-*` to the
existing content volume. The application needs the bundled-library support in
CoJudge commit `b58c197` or later. Keep learner progress files intact.
