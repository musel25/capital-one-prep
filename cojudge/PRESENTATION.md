# Problem presentation

Custom problem pages follow the source exercise format: context, a direct task,
concrete examples, and brief input guarantees where needed. Original Pybites task
text stays visible. The page supplies the title, so statements do not repeat it.

`cojudge/presentation.py` extracts the actual Python checks for the Test Case
panel. Each course's `present_problem(spec, test_ids)` supplies:

- `statement`: the main task and necessary input guarantees.
- `examples`: real calls, requests, or commands with expected results.
- `testCaseDescriptions`: actual check code keyed by the internal test selector.
- `courseHelp`: optional instructions, runtime details, and source notes.

Use the course's examples module for manually expected examples. Tests execute
these examples against the reference code. Do not replace the original task with
a second specification. Keep operation and migration instructions in course help.

Refresh presentation fields without rebuilding execution files:

```bash
uv run python scripts/refresh_custom_presentations.py
uv run python scripts/refresh_custom_presentations.py --check
```

The refresh checks that starter code, test inputs, marker files, solutions, and
bundled libraries remain unchanged. It covers the nine active custom lists and
135 problems. It does not add retired course indexes or modify learner data.
