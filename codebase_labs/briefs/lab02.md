# lab02: Parameterize the runtime boundary

[Back to the ordered course guide](../README.md)

**Objective:** Use parametrized tests to distinguish runtime types from type annotations.

**Practice estimate:** 35 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab02
```

Open the printed folder and follow its README. It includes the exact check command.

## Context

This constructed intake snapshot loads a retry setting.
It is not a Capital One question. It is independent of lab01.
This snapshot has a different documented default and range.
The application is correct. Write tests for its runtime boundary.
This lab does not model parsing JSON, a network, or static type checking.

## Learn first

A type annotation describes an intended type.
It does not reject a value when Python calls a function.
Runtime validation checks the actual value during execution.
Python treats `bool` as a subclass of `int`.
The product rule can still reject booleans.

Work through this trace: `load_settings({"retries": 4})` reads `4`.
`validate_retries` accepts it. `IntakeSettings` stores `4`.
The caller can read the result through `.retries`.
No conversion from a string or float is part of this contract.

A parametrized test runs one test function with several named inputs.
`@pytest.mark.parametrize("value", values)` supplies one value per case.
Use `ids=` to give useful case names in failure reports.
Put accepted inputs and rejected inputs in separate test functions.
Use `pytest.raises(ValueError)` for each rejected value.
The public test shows parametrization on two ordinary accepted values.
Choose expected outcomes from the product rule, not from the implementation.

## File map

- `app/__init__.py`: package marker.
- `app/validation.py`: `validate_retries`, the runtime boundary.
- `app/models.py`: `IntakeSettings`, the returned data object.
- `app/service.py`: `load_settings`, the entry point and missing-key default.
- `tests/test_existing.py`: a small parametrized example.
- `tests/learner/test_task.py`: your test file.

## Read and trace

Run `rg -n "retries|validate_retries" app`.
Trace how `load_settings` calls the validator.
Locate the default and the numeric range in their separate files.
Predict what a type annotation does when the caller passes `"4"`.

## Assignment and allowed edits

Write your own parametrized boundary tests in `tests/learner/`.
Test the validator directly. Add a small entry-point test for key presence.
Include both ends of the valid range and all listed rejected classes.
Only `tests/learner/` is editable.
Do not change application files or existing tests.

## Exact behavior

`validate_retries(value)` accepts only built-in integers from `0` through `5`.
It returns the same numeric value as a built-in integer.
It rejects booleans, integer subclasses, floats, strings, `None`, lists,
dictionaries, negative integers, and integers above `5` with `ValueError`.
Error-message text is not part of the contract. No value coercion is allowed.
Custom integer subclasses are outside the required learner test matrix.

`load_settings(payload)` accepts a built-in dictionary.
An absent `retries` key supplies `3`.
A present value goes through `validate_retries`, including `None` and zero.
The result is an `IntakeSettings` object with the validated `.retries` value.
Unknown keys are ignored. The payload stays unchanged.
Other payload-container types are outside scope.

## Examples

- `{}` gives `.retries == 3`.
- `{"retries": 0}` gives `.retries == 0`.
- `{"retries": 5}` gives `.retries == 5`.
- `{"retries": None}` raises `ValueError`.
- `True`, `"3"`, `3.0`, `-1`, and `6` each fail direct validation.

## Boundary checklist

- Boolean values detect an overly broad integer check.
- Numeric strings detect silent text conversion.
- Whole and fractional floats detect silent numeric conversion.
- `5` and `6` detect an incorrect inclusive upper limit.
- Zero, negative values, null, and containers cover other boundary classes.
- Missing, null, and zero must be separate service cases.

## Commands

Run from the new lab directory.

```sh
uv run pytest -q tests/test_existing.py
uv run pytest --collect-only -q tests/learner
uv run pytest -q tests/learner
uv run pytest -q tests/learner -k rejects
uv run pytest -q
git diff -- app tests/learner
```

Inspect the collected case names before running the suite.
Read an assertion failure to find the smallest input that breaks a rule.
New untracked test files need direct file review as well as `git diff`.

## Optional AI review

"Review my boundary table against app/validation.py and app/service.py.
Cite the file and function for each rule. Identify one missing input class.
Do not write tests or implementation. I will write all code."

Constructed AI claim to check: "The annotation `value: int` and
`isinstance(value, int)` together ensure that boolean values are rejected."

## Hints

First, classify each input by runtime type before checking its numeric value.
Next, choose values just inside and just outside the range.
Finally, verify that your rejection cases actually execute the call.
Do not use `xfail` for behavior that the contract requires.

## Done checks

Accepted cases assert values and output types.
Rejected cases assert `ValueError`.
Your suite has separate boolean, text, float, and range cases.
Correct code passes. Each faulty validator causes an assertion failure.
A test count does not show that all boundary classes are covered.

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> The annotation value: int and isinstance(value, int) together ensure that boolean values are rejected.

## Official references

- [Documentation 1](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [Documentation 2](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)
