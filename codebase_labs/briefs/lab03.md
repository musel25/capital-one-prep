# lab03: Repair state leakage between queues

[Back to the ordered course guide](../README.md)

**Objective:** Write a regression test and repair ownership of mutable instance state.

**Practice estimate:** 45 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab03
```

Open the printed folder and follow its README. It includes the exact check command.

## Context

This is a constructed exercise. It is not a Capital One question.
Each intake queue belongs to one owner and holds that owner's labels.
The starter passes the public test. It has a disclosed state-isolation defect.
Operations on one queue can affect another queue.
This independent snapshot does not model threads, persistence, or shared queues.

## Learn first

State is data that remains between method calls.
A mutable object can change after it is created. A list is mutable.
An instance is one object created from a class.
A class attribute can be shared by all instances.
An instance attribute belongs to one instance.
Two different attribute names can still refer to the same list.

A regression test reproduces a defect before the repair.
It then protects the repaired behavior.
Write that test first. Confirm an assertion failure before editing the source.

Work through a correct single-queue example.
`queue = IntakeQueue(" desk ")` creates owner `"desk"` with no labels.
`record(queue, " draft ")` returns `{"owner": "desk", "labels": ["draft"]}`.
A second record of `"draft"` keeps both entries.
This example does not prove that two queues are independent.

A snapshot is a returned view of state at one time.
This contract requires a detached dictionary and a detached labels list.
A shallow list copy is sufficient here because each label is a string.
This rule would need more analysis if labels contained mutable nested data.

## File map

- `app/__init__.py`: package marker.
- `app/validation.py`: `clean_text`, required text validation.
- `app/queue.py`: `IntakeQueue`, label ownership and snapshots.
- `app/service.py`: `record`, the public composition of add and snapshot.
- `tests/test_existing.py`: the supported single-queue path.
- `tests/learner/test_task.py`: your regression and compatibility tests.

## Read and trace

Run `rg -n "class |def |labels|clean_text" app`.
Trace `record` through `add` and `snapshot`.
Find every place where a labels list is created, changed, or returned.
Predict the results for two queues before you run your regression.
Test two live instances in one test. Separate tests can hide their relationship.

## Assignment and allowed edits

Write a failing regression in `tests/learner/` before the repair.
Repair state ownership only in `app/queue.py`.
Preserve validation, order, duplicates, and detached snapshots.
Do not change method names, parameters, return shapes, or the other app files.
Do not clear global state in test setup to hide leakage.
Do not edit the public tests or runner files.

## Exact behavior

`IntakeQueue(owner)` starts with an empty history for that instance.
An owner must be a string with text after stripping outside whitespace.
Store the stripped owner. Preserve its case.
Missing text, non-string values, and whitespace-only text raise `ValueError`.
Error-message text is not part of the contract.

`add(label)` applies the same text rule to a label.
A valid call appends one stripped label and returns `None`.
Preserve insertion order and duplicates. Preserve case.
A rejected call raises `ValueError` and leaves state unchanged.
`snapshot()` returns exactly `{"owner": <owner>, "labels": <list>}`.
Editing a returned dictionary or list must not change the queue.
Later queue changes must not change an earlier snapshot.
Constructing or changing any queue must not change another queue.
This also applies when two queues have the same owner text.
`record(queue, label)` adds the label and returns the resulting snapshot.

## Examples

- Two new queues each start with `labels == []`.
- Add `"red"` to the first. The second still has `labels == []`.
- Create a third queue. The first still has `labels == ["red"]`.
- Change a returned list. A new snapshot still shows the queue's own labels.
- Add `" "`. The call raises `ValueError` and preserves the previous history.

## Boundary checklist

- Two existing queues with interleaved writes detect shared state.
- Creating a later queue detects a repair that clears a shared list.
- Editing a returned list detects a snapshot that exposes live state.
- Repeated labels and rejected additions protect existing behavior.

## Pytest lesson and commands

Keep arrange, act, and assert visible in each test.
Arrange means create the input objects. Act means call the application.
Assert means compare the observed result with an independent prediction.
A function-scoped fixture creates fresh test data for each test.
You may use a fixture for repeated setup, but do not hide the two-queue scenario.

Run from the new lab directory.

```sh
uv run pytest -q tests/test_existing.py
uv run pytest --collect-only -q tests/learner
uv run pytest -q tests/learner
uv run pytest -q tests/learner -k queue
uv run pytest -q
git diff -- app/queue.py tests/learner
```

Run the focused suite before and after the repair.
Record the failing test name and actual output in your test-file docstring.
New untracked files may need direct review because `git diff` omits them.

## Optional AI review

"Review my regression and my diff for state ownership. Cite the file,
class, and method behind each concern. Check whether two live instances
can still affect each other. Do not write the fix or tests. I will write all code."

Constructed AI claim to check: "Clearing the labels list in `__init__`
gives every new queue a clean list, so it fixes state isolation."

## Hints

First, inspect where the list is allocated.
Next, compare construction before a write with construction after a write.
Finally, check ownership at the snapshot boundary as well as the instance boundary.

## Done checks

Your own regression failed by assertion before the repair.
It passes after the repair. Public tests also pass.
The checker accepts the behavior and rejects all faulty variants with your tests.
Your diff changes only queue ownership and your test files.
No test depends on another test running first.

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> Clearing the labels list in __init__ gives every new queue a clean list, so it fixes state isolation.

## Official references

- [Documentation 1](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables)
- [Documentation 2](https://docs.pytest.org/en/stable/how-to/fixtures.html)
