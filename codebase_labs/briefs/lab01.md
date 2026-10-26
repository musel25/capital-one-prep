# lab01: Trace the intake pipeline

[Back to the ordered course guide](../README.md)

**Objective:** Trace a public entry point and write characterization tests for its behavior.

**Practice estimate:** 35 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab01
```

Open the printed folder and follow its README. It includes the exact check command.

## Context

This is a constructed exercise. It is not a Capital One question.
A small intake application prepares requests for a queue.
The application is correct. Your task is to protect its behavior with tests.
This snapshot is independent of other labs.
It does not model a database, an HTTP API, or actual queue delivery.

## Learn first

An entry point is the function that a caller uses first.
A pipeline passes data through several functions.
A characterization test records behavior that already exists.
It gives evidence about compatibility when the implementation changes.

Trace one example before you run it.
For `{"owner": "  LEE ", "retries": 1}`, the owner becomes `"lee"`.
The retry count stays `1`. The route becomes `"queue"`.
The result is `{"owner": "lee", "retries": 1, "route": "queue"}`.
The original dictionary stays unchanged.

Pytest collects functions whose names start with `test_`.
Use `assert actual == expected` to compare an output with your prediction.
Use `with pytest.raises(ValueError):` around a call that must be rejected.
Indent only the call inside that block.
The public test demonstrates an assertion on a separate basic case.
If a test fails, read the assertion values and the last application frame
in the traceback. A traceback lists the calls that led to a failure.

## File map

- `app/__init__.py`: package marker.
- `app/service.py`: `prepare_request`, the public entry point.
- `app/normalize.py`: `clean_owner`, the text transformation.
- `app/config.py`: `read_retries`, configuration validation and defaults.
- `tests/test_existing.py`: one supported path and basic pytest syntax.
- `tests/learner/test_task.py`: your empty test file.

## Read and trace

Run `rg -n "def |from app" app` to find functions and imports.
Read `prepare_request` first. Follow its two imported functions.
Write a short call map in your test-file docstring.
Predict a zero-retry request before running it.
Find where a blank owner stops the pipeline.

## Assignment and allowed edits

Write your own tests in `tests/learner/`.
Test `prepare_request` so that the real helpers run together.
Include a transformation, a default, an explicit zero, and a rejection.
Check that the caller's input does not change.
Do not edit `app/`, the public tests, or runner files.

## Exact behavior

Input is a built-in dictionary. Other input-container types are outside scope.
`owner` is required. It must be a string with text after `strip()`.
The output owner is `owner.strip().lower()`.
A missing owner, `None`, a non-string, or a whitespace-only string raises
`ValueError`. Error-message text is not part of the contract.
An absent or `None` retry value means `2`.
Otherwise, retries must be a built-in integer from `0` through `3`.
Booleans, strings, floats, and values outside that range raise `ValueError`.
A zero retry count selects `"manual"`. All other accepted counts select `"queue"`.
Return a new dictionary with exactly `owner`, `retries`, and `route`.
Ignore unknown input keys. Do not change input on success or rejection.

## Examples

- `{"owner": "Sam"}` produces `{"owner": "sam", "retries": 2, "route": "queue"}`.
- `{"owner": "Sam", "retries": None}` produces the same result.
- `{"owner": "Sam", "retries": 0}` produces `{"owner": "sam", "retries": 0, "route": "manual"}`.
- `{"owner": " "}` raises `ValueError`.

## Boundary checklist

- Uppercase text plus outside whitespace detects a missing transformation.
- An explicit zero detects a default based only on truthiness.
- A whitespace-only owner detects a missing rejection.
- Missing and null retry values check the documented default.
- Saved input values check the no-mutation rule.

## Commands

Run these commands from the new lab directory.

```sh
uv run pytest -q tests/test_existing.py
uv run pytest --collect-only -q tests/learner
uv run pytest -q tests/learner
uv run pytest -q tests/learner -k zero
uv run pytest -q
git diff -- app tests/learner
```

`--collect-only` lists discovered tests without running them.
`-k zero` runs test names that contain `zero`.
A new untracked file might not appear in `git diff`.
Read your file directly in that case.

## Optional AI review

"Explain the path from prepare_request to its helpers. Cite file names
and function names. Review my written test cases for one missing input
class. Do not write implementation code or tests. I will write all code."

Constructed AI claim to check: "The expression `value or 2` preserves
all valid retry values because the default is also an integer."
Predict a counterexample before checking the claim with your own test.

## Hints

First, compare a missing key with an explicit value.
Next, record a literal expected dictionary before calling the entry point.
Finally, keep the real helpers in the test path.
A test of a helper alone cannot prove that the entry point calls it.

## Done checks

Your tests pass on the supplied application.
Your tests collect as actual tests.
Your call map matches the imports and calls in the source.
The checker rejects each supplied class of faulty behavior by an assertion.
A pass covers these sampled rules. It does not prove all possible behavior.

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> The expression value or 2 preserves all valid retry values because the default is also an integer.

## Official references

- [Documentation 1](https://docs.pytest.org/en/stable/how-to/assert.html)
