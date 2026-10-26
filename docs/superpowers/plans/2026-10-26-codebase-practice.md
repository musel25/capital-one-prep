# Codebase Practice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Publish a progressive course for reading code, writing effective tests, making scoped changes, and checking AI claims.

**Architecture:** Sixteen CoJudge exercises reuse verified behavioral oracles with new guided repair starters and lessons. Eight independent local labs use a common safe attempt runner and instructor-only reference, contract, and mutation material. A single guide interleaves the browser tasks and labs.

**Tech Stack:** Python 3.11-compatible browser code; Python >=3.12, uv, pytest, FastAPI, and httpx locally; existing native CoJudge content format and Java markers.

**Spec:** `docs/superpowers/specs/2026-10-26-codebase-practice-design.md`

## Global Constraints

- Preserve attempts and private notes. Create unique new attempts only on user start.
- Learners write code and tests; AI prompts request explanations or reviews, never implementation.
- Publish under new `cb-*` IDs and `capital-one-codebase-practice` course ID.
- Keep earlier courses available. Do not require SQL or advanced system design.
- Use deterministic data and dependencies. No live network or real sleep in exercises.
- Use uv for Python commands. Commit coherent units and push immediately.
- Keep instructor source out of learner folders. Check temporary copies only.
- State the limits of behavior checks. Do not promise interview readiness.

## Review Focus

- Empty or skipped learner tests must not pass a testing exercise.
- Import/collection/setup errors must not count as detecting a faulty implementation.
- Repeated starts, malformed manifests, and symlinks must not overwrite or read unrelated learner files.
- New metadata, course links, and completion IDs must not point to the old course by accident.
- Correct-looking AI changes must have a concrete counterexample independent of the proposed change.

---

### Task 1: Complete the earlier live verification

**Files:** `scripts/check_cojudge_live.py`, `tests/test_cojudge_live.py`, `cojudge/verification.*`, `cojudge/README.md`.

- [x] Add tests for manual review cases, all mutations, and rejection of infrastructure failures as evidence.
- [x] Extend `check_live(spec, base_url, review_cases=None)` to implement those checks.
- [x] Run repository tests: 61 passed before the curriculum revision.
- [x] Finish all 50 live checks on the current deployment and save the actual report.
- [x] Record results, commit `test: complete live review and mutation checks`, and push (5355aa7).

### Task 2: Define and review the curriculum

**Files:** design and this plan; `codebase_labs/CONTRACT.md`.

- [x] Write the design with exact format, sequence, user work, and verification limits.
- [x] Obtain the brainstorming skill's independent builder check: no material gaps.
- [x] Define the lab authoring interface below and commit the design/plan/contract.
- [x] Push before implementation.

### Task 3: Create the guided browser course

**Files:** `cojudge/codebase/lessons.py`, `cojudge/codebase/support.py`, `scripts/codebase_course.py`, shared `cojudge/authoring/support.py`, `tests/test_codebase_course.py`, generated `cojudge/problems/cb-*` and course files.

**Interfaces:** Lesson entries contain `number`, `source_number`, `title`, `orientation`, `read`, `scope`, `test_plan`, `ai_prompt`, `ai_claim`, `ai_answer`, and `done`. `load_codebase_specs()` produces the existing SPEC shape with `prefix='cb'`, new `course_id`, `category`, and `level`. Preserve the original input contract, cases, Java oracle, and reference. Build the starter from a verified realistic mutation plus orientation comments.

- [x] Test a new problem has new ID/category/course links while old metadata remains unchanged.
- [x] Add optional validated metadata overrides in the shared builder with old defaults.
- [x] Write sixteen concrete lesson overlays following the source mapping in the design.
- [x] Add source provenance and independent review-case mapping.
- [x] Add build/verify/live subcommands. Live checks reuse `check_live` with review cases.
- [x] Verify all new starters expose wrong behavior, all references pass, and all Java oracles agree.
- [x] Commit the verified course authoring and generated content; push.

### Task 4: Author the local labs

**Files:** `codebase_labs/lab01.py` through `lab08.py`.

**Interfaces:** Follow `codebase_labs/CONTRACT.md`. Each exports a self-contained LAB dictionary. Author labs 01–04 and 05–08 independently. No agent changes the runner or other lab files.

- [x] Write exact contracts, small multi-file source snapshots, public tests, learner test stubs, sample instructor tests, and realistic faulty variants.
- [x] Include hand-derived expectations for empty, boundary, invalid, repeated, isolation, and side-effect cases where valid.
- [x] Verify every public test passes the assigned starter and the correct reference.
- [x] Verify sample learner tests accept correct code and reject every named faulty variant through assertions.
- [x] Keep all instructor code outside the generated learner files.
- [x] Review the lesson scope, technical accuracy, and AI claim counterexamples.

### Task 5: Implement the local runner

**Files:** `codebase_labs/runner.py`, `scripts/codebase.py`, `tests/test_codebase_labs.py`.

**Interfaces:** `load_labs() -> list[dict]`, `start(lab_id, output_root) -> Path`, `check(path) -> dict`, `verify() -> dict`. CLI list/start/check/verify; exit 0 success, 1 missing behavior/test evidence, 2 setup/execution error.

- [x] Test two starts create different folders and preserve the first folder's contents.
- [x] Test generated attempts exclude reference, contracts, variants, and sample answer tests.
- [x] Test manifests and symlinks reject unsafe paths; check leaves all attempt hashes unchanged.
- [x] Test empty/skipped tests, correct tests, weak tests, and collection failures produce distinct failures.
- [x] Copy attempts to temporary directories and run uv/pytest with local imports.
- [x] Grade learner tests against reference and faulty variants using pytest JUnit results; require assertion failures and at least one passing learner test on the reference.
- [x] Run separate contract checks for repair/feature labs on learner code.
- [x] Verify all eight starter/reference/sample-test combinations with the same checker used by learners.
- [x] Commit labs and runner together after integrated review; push.

### Task 6: Publish the guide and course

**Files:** `codebase_labs/README.md`, repository README, course description and statements, `cojudge/codebase/verification.json`, `cojudge/codebase/verification.md`.

- [x] Write the exact interleaved sequence: four browser tasks, two local labs, repeated four times.
- [x] Give start/check commands, technical skill map, and how to use AI without delegating implementation.
- [x] Run repository Python tests and any affected frontend checks.
- [x] Publish new problem directories to the current runtime volume.
- [x] Run all sixteen references, examples, review cases, and faulty variants through live endpoints.
- [x] Publish the new course index only after live verification passes.
- [x] Verify file hashes, course order, guide links, and preservation of existing courses.
- [x] Save actual evidence and limits. Commit and push.

Completed October 26, 2026. See `cojudge/codebase/verification.md` and
`cojudge/codebase/verification.json` for actual checks and limits.
