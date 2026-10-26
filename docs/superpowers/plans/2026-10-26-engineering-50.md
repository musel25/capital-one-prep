# Engineering 50 Implementation Plan

> **For agentic workers:** Use the parallel-agent skill for independent content groups. Use fresh review for the final pack.

**Goal:** Publish 50 verified technical problems as a custom CoJudge course.

**Architecture:** Version a self-contained content pack in this repository.
A local builder generates native CoJudge files from authored problem modules.
The existing server loads the pack from its persistent content volume.

**Tech Stack:** Python standard library, Java reference markers, CoJudge.

**Spec:** `docs/superpowers/specs/2026-10-26-engineering-50-design.md`

## Global constraints

- Preserve all existing attempts, notes, and courses.
- Python 3.11 compatible learner code; use `uv run` for local Python.
- Exactly 50 ordered original problems, split into five levels.
- Actual SQLite in database reference solutions; simulated network/concurrency.
- At least 12 explicit and 12 additional distinct test inputs per problem.
- One realistic rejected mutation per problem; optional revealed solutions.
- Commit coherent units and push each commit immediately.

## Review focus

- JSON comparison must distinguish booleans from integers and preserve lists.
- Retries must not repeat writes; duplicate IDs with different bodies conflict.
- Money and TTL boundaries must use exact specified rules.
- SQL exercises must cover empty tables, NULL, duplicates, and rollback.
- Publish only new namespaced paths after live judge checks pass.

## Tasks

- [x] Build and test the authoring adapter, Java JSON support, and local verifier.
  Files: `cojudge/authoring/support.py`, `cojudge/authoring/Support.java`,
  `scripts/build_cojudge.py`, `scripts/verify_cojudge.py`, `tests/test_cojudge.py`.
  Test wrong output types, JSON formatting, deterministic generation, and guards.
- [x] Author 01–20 in `cojudge/authoring/p01.py` through `p20.py`.
  Cover data boundaries, standard libraries, typed models, objects, inheritance,
  mutation, invariants, and idempotency. Verify explicit cases and mutations.
- [x] Author 21–35 in `cojudge/authoring/p21.py` through `p35.py`.
  Cover HTTP contracts, retries, caching, pagination, and initial SQL tasks.
  Verify explicit cases and mutations.
- [x] Author 36–50 in `cojudge/authoring/p36.py` through `p50.py`.
  Cover database transactions, version conflicts, queues, and system components.
  Verify explicit cases and mutations.
- [x] Review contracts, pedagogy, independent references, and test diversity.
  Build all content; run `uv run python scripts/verify_cojudge.py` and focused pytest.
- [ ] Stage content on the server, run every reference through the live judge,
  and reject a wrong solution for every problem. Publish the course index last.
  Verify the course and problem HTML. Add a repository README link. Commit and push.
