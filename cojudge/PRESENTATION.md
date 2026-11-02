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

## Focus and supplied helpers

Each exercise practises one target skill, such as `@classmethod` or a
`defaultdict` grouping. Work that is not the target skill goes into the starter
as small, finished helpers. Examples are regex checks, URL and CSV parsing, text
cleanup, tie rules, and test data. A `# FOCUS:` and `# SUPPLIED:` comment block
above the helpers names both parts. The reference solution uses the same
helpers. Deliberate faults target the learner's part, not the helpers. The first
hint names the target skill. When you add an exercise, apply the same split.

Refresh presentation fields without rebuilding execution files:

```bash
uv run python scripts/refresh_custom_presentations.py
uv run python scripts/refresh_custom_presentations.py --check
```

The refresh checks that starter code, test inputs, marker files, solutions, and
bundled libraries remain unchanged. It covers the nine active custom lists and
135 problems. It does not add retired course indexes or modify learner data.

### Publication — November 1, 2026

The 39 selected exercises with focus hints and supplied helpers are published.
The live judge accepts every reference and rejects every starter in the OOP,
Collections, Data Formats, Decorators and Pytest courses. In the Decorators
course, it also rejects every prepared fault.
Private backup of the replaced problem folders:
`/home/ubuntu/cojudge-backups/focus-helpers-20261101.vDcT7G/old/`.
Learner progress and saved code were not changed.
