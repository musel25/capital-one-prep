# lab04: Test a caller with a fake dependency

[Back to the ordered course guide](../README.md)

**Objective:** Test real caller behavior with an injected fake and a narrow exception boundary.

**Practice estimate:** 40 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab04
```

Open the printed folder and follow its README. It includes the exact check command.

## Context

This is a constructed exercise. It is not a Capital One question.
The intake service validates a request and sends a record through a gateway.
This independent snapshot is correct. Your task is to test the caller.
A gateway is the boundary through which the service sends data.
This lab has no real network, timer, persistence, or automatic retry loop.

## Learn first

A dependency is an object that another object calls to do part of its work.
Dependency injection means passing that object into the caller.
`IntakeService(gateway)` makes this boundary explicit.
A fake is a small test implementation of that boundary.
It can record calls, return a chosen receipt, or raise a chosen exception.
Keep `IntakeService.submit` and real validation in the test path.

Work through a success example.
The input owner `"  REI "` becomes `"rei"`.
With no retries key, the gateway receives `{"owner": "rei", "retries": 2}`.
If the gateway returns `"r-12"`, the service returns
`{"status": "accepted", "owner": "rei", "receipt": "r-12"}`.
One recorded call proves that this real caller sent one record.
Calling the fake directly would only test the fake.

An exception boundary determines which failures a caller handles.
Here, only `GatewayUnavailable` becomes a retry result.
Other exceptions must stay visible to the calling code.
A result named `"retry"` does not mean that the service makes another call.

## File map

- `app/__init__.py`: package marker.
- `app/service.py`: `IntakeService`, the real caller under test.
- `app/validation.py`: `prepare_payload`, validation and normalization.
- `app/gateway.py`: `Gateway` protocol and a local `MemoryGateway`.
- `app/errors.py`: `GatewayUnavailable`, the one handled exception class.
- `tests/test_existing.py`: a supported path with the local gateway.
- `tests/learner/test_task.py`: your fake and your tests.

## Read and trace

Run `rg -n "def |send|except|prepare_payload" app`.
Trace validation, the dependency call, and both return paths.
Inspect which code is inside the `try` block.
Predict what happens when the gateway raises `ValueError`.
Compare that with invalid input that raises before a gateway call.

## Assignment and allowed edits

Write a small fake and your own tests in `tests/learner/`.
Pass the fake to the real `IntakeService` constructor.
Test success, the handled exception, an unexpected exception, and invalid input.
Assert exact calls and arguments where the contract requires them.
Do not replace the service, its `submit` method, or the validator with a fake.
Only `tests/learner/` is editable.

## Exact behavior

Input is a built-in dictionary. Other container types are outside scope.
Owner is required and must be a string with text after `strip()`.
Normalize it with `strip().lower()`.
A missing owner, non-string owner, or blank owner raises `ValueError`.
Missing or `None` retries means `2`.
Other retry values must be built-in integers from `0` through `5`.
Booleans, strings, floats, and out-of-range integers raise `ValueError`.
Error-message text is not part of the contract.
Ignore unknown keys. Keep the caller's dictionary unchanged on all paths.

Invalid input must produce zero gateway calls.
Valid input must produce exactly one `gateway.send(record)` call.
Its argument must contain exactly the normalized `owner` and `retries`.
The gateway returns a receipt string or raises an exception.
A receipt produces exactly `status`, `owner`, and `receipt` in the response.
Use status `"accepted"` and preserve the exact receipt string.
`GatewayUnavailable`, including its subclasses, produces exactly
`{"status": "retry", "owner": <normalized owner>}`.
Do not include a receipt on that path. Do not make another gateway call.
Every other gateway exception propagates as the same exception object.
Custom gateways that mutate the supplied record are outside scope.

## Examples

- Owner `" A "`, retries `0`: send `{"owner": "a", "retries": 0}` once.
- Gateway returns `"job-8"`: return that exact receipt with status `"accepted"`.
- Gateway raises `GatewayUnavailable`: return status `"retry"` with no receipt.
- Gateway raises `ValueError`: propagate it. Do not return status `"retry"`.
- Owner is `" "`: raise `ValueError` before any gateway call.

## Boundary checklist

- An unexpected exception detects a catch that is too broad.
- Mixed-case input and an unknown key detect an unprocessed gateway argument.
- Exact call count detects a duplicate send.
- Blank input and zero calls detect missing validation before a side effect.
- The handled exception must produce the exact response without a hidden retry.

## Pytest lesson: fakes and patch lookup

Keep each fake small. Give it a call list and a configured outcome.
Use a fresh fake for each test so that call history cannot leak between tests.
Use `pytest.raises` for an exception that must propagate.
You can use `as caught` to inspect the exception object.

Patching is another way to replace a dependency temporarily.
Patch the name where the caller looks it up.
For example, this service imports `prepare_payload` into `app.service`.
Replacing `app.validation.prepare_payload` after that import would not
replace the name already held by `app.service`.
Its lookup name is `app.service.prepare_payload`.
Keep that function real for this assignment. Constructor injection already
gives you the gateway boundary without a patch.

## Commands

Run from the new lab directory.

```sh
uv run pytest -q tests/test_existing.py
uv run pytest --collect-only -q tests/learner
uv run pytest -q tests/learner
uv run pytest -q tests/learner -k exception
uv run pytest -q
git diff -- app tests/learner
```

Read new untracked files directly if they do not appear in `git diff`.

## Optional AI review

"Review my fake and my tests. Cite the file and function for the real
caller path. Check whether my tests preserve validation and test the
exception boundary. Do not write code or tests. I will write all code."

Constructed AI claim to check: "Catching every exception from send is
safer because every gateway failure should become a retry response."

## Hints

First, make a fake return a receipt that the source cannot predict.
Next, record arguments before the fake returns or raises.
Finally, use separate cases for a known outage and an unexpected adapter error.
Do not infer the call count only from the returned response.

## Done checks

The real service and validation run in every caller test.
Success and both exception classes have explicit output or exception assertions.
Invalid input has an explicit zero-call assertion.
Correct code passes. Every supplied faulty variant fails by assertion.
Passing fake-based tests does not verify a real external gateway.

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> Catching every exception from send is safer because every gateway failure should become a retry response.

## Official references

- [Documentation 1](https://docs.pytest.org/en/stable/how-to/assert.html)
- [Documentation 2](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
