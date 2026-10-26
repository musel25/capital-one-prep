# Codebase Practice publication and verification

[Open the published course](https://cojudge.musel.dev/?course=capital-one-codebase-practice).
The [full guide](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md)
interleaves 16 browser exercises and eight local labs.

Verified on October 26, 2026:

| Check | Result |
| --- | --- |
| Browser references checked locally in Python and Java | 16 passed |
| Official browser cases | 449 passed locally and through live Submit |
| Manual review cases, including worked traces and AI claims | 56 passed in Python, Java, and live Run |
| Live sample executions | 48 passed |
| Faulty browser variants | All 17 rejected by wrong answers locally and live |
| Runnable repair starters | All 16 expose incorrect behavior |
| Local labs checked through the learner checker | All eight passed with completed sample attempts |
| Sample learner tests on correct local implementations | 69 passed |
| Faulty local implementations | All 28 detected through assertions |
| Repository regression tests | 77 passed |
| Problem HTTP pages, titles, lessons, and course links | All 16 checked |
| Published problem files compared with local SHA-256 hashes | 80 matched |
| Published course file | SHA-256 matched |
| Selected course and problem order in server data | Correct; all 16 in order |
| Existing course files | All six unchanged |
| Earlier problem files after shared-builder changes | All 250 regenerate without changes |
| Public guide and eight learner briefs | Present on the repository's main branch |

The independent review found stale prerequisites and a checker classification
error. Both were corrected before publication. The regression test for the
checker failed before the fix and passed after it. See [review.md](review.md).
Machine-readable evidence is in [verification.json](verification.json).

Commands used:

```sh
uv run python scripts/codebase_course.py build
uv run python scripts/codebase_course.py verify --report /tmp/codebase-course-verified.json
uv run python scripts/codebase.py verify --report /tmp/codebase-labs-verified.json
uv run pytest -q
uv run python scripts/codebase_course.py live \
  --base-url http://127.0.0.1:15379 --report /tmp/codebase-course-live.json
```

The active site was `cojudge-profiles` on server port 5379. Local port 15379 was
an authorized SSH tunnel. Only the new `cb-*` problem files and new course index
were published. The index was published after all live checks passed. No profile
progress endpoint was called. Existing learner attempts and notes were not read
or changed. No upstream app code or authentication configuration was changed.

Run and Submit were checked through the endpoints used by the interface. Page
checks used HTTP and server course data. Interactive browser automation was not
available, so this is not a claim of interactive editor UI testing.

The browser judge checks outputs, not reasoning, architecture, type annotations,
or test quality. The local checker checks selected behavior and prepared faulty
variants. Neither finite checks nor course completion prove interview readiness.
