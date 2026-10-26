# Publication and verification — 2026-10-26

[Capital One Engineering 50 is live](https://cojudge.musel.dev/?course=capital-one-engineering-50).
The existing site login remains in place.

| Check | Result |
| --- | --- |
| Original problems | 50, in five ordered levels |
| Official cases checked locally in Python and Java | 1,515 passed |
| Additional independent reviewer cases | 51 passed in both languages |
| Realistic faulty variants checked locally | 51 rejected |
| Live CoJudge Run with each reference | 50 passed; 150 sample executions |
| Live CoJudge Submit with each reference | 50 passed; all 1,515 official cases |
| Live Submit with a faulty variant for each problem | 50 rejected |
| Problem page HTTP and lesson checks | 50 passed |
| Deployed problem files compared with local SHA-256 hashes | 250 matched |
| Course selector and server course data | Active course; all 50 problems in order |
| Existing course files | All five SHA-256 hashes unchanged |
| Repository regression suite | 55 pytest tests passed |
| Content regeneration | No difference after rebuilding |

The local verifier also rejects malformed JSON and incorrect output types.
The independent review confirmed that every faulty variant has an explicit
case that returns a wrong answer without needing a crash. See
[review.md](review.md) for the defects found and corrected. Machine-readable
results, the content commit, and per-problem live counts are in
[verification.json](verification.json).

Commands used from the repository root:

```bash
uv run python scripts/verify_cojudge.py --report /tmp/cojudge-verified-final.json
uv run python scripts/build_cojudge.py
uv run pytest -q
uv run python scripts/check_cojudge_live.py \
  --base-url http://127.0.0.1:15376 --report /tmp/cojudge-final-live.json
```

Port 15376 was an SSH tunnel bound to local loopback. It forwarded to the
existing server at 127.0.0.1:5376. No authentication setting was changed.
The live judge used its installed Python 3.11 and Java 22 containers.

Only the new `c1-*` problem directories and the new course directory were
published to `/data` in the existing `cojudge` container. The course index was
published after all live checks passed. Instructor artifacts were not copied
to the site's content directory. Browser progress and learner attempts were
not modified.

## Runner conflict found during verification

The server also had an unrouted `cojudge-trial` container on port 5375. Its
orphan cleanup selected all containers with `cojudge.created=true`, including
active runners owned by the main site. Its logs showed it stopping the main
site's Python and Java runners. This caused the first live attempt for problem
01 to fail before execution.

Stopped `cojudge-trial`. The routed `cojudge` instance on port 5376 stayed
running. The trial instance uses the `unless-stopped` restart policy. Its
files and volume were retained. The full 50-problem live verification then
passed. Do not run the two instances together until their orphan cleanup is
scoped to the owning session. No upstream CoJudge source was changed.

## Verification limits

The page checks inspected HTTP responses, rendered headings, the active course
tab, and the ordered server data. Browser interaction automation was unavailable
in this session. Run and Submit were tested through the live endpoints used by
the interface.

Passing finite tests does not prove every possible solution correct. The output
judge cannot certify type annotations, inheritance, SQL use, or complexity.
API and system problems use controlled simulations. SQL reference solutions
use real in-memory SQLite. These checks do not certify interview readiness.
