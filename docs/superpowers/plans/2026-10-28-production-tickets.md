# Production Tickets and Pybites Checks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace three live course lists with 24 concise Python software engineering tickets and strengthen all 22 Pybites exercises.

**Architecture:** Keep content authoring in this repository. Reuse the existing independent Java marker and JSON verification utilities. Publish only native problem files and course indexes to the existing VPS content volume.

**Tech Stack:** Python 3.11 learner code, uv, Java markers, existing CoJudge API.

**Spec:** The user requests LeetCode-style input/output statements, practical production work, removal of Codebase Practice / Capital One Engineering 50 / Python OOP, and Pybites tests or explicit input guarantees.

## Global Constraints

- Preserve learner solutions, progress, other courses and `attempts/`.
- No new learner dependencies or network access.
- Each ticket has one clear interface, short context, examples, and explicit input bounds.
- Keep Pybites public behavior; clarify unsupported inputs rather than adding arbitrary validation.
- Commit each coherent unit and push immediately.
- Work in the existing checkouts. Changes are content-only; no app rebuild is needed.

## Review Focus

- Empty strings and collections: support them or explicitly exclude them.
- Exact expiry and window boundaries: state and test inclusive/exclusive behavior.
- Duplicate messages and idempotency keys: test state after repeats and conflicts.
- Independent calls: prevent shared state and input mutation.
- Saved Pybites editors contain old test blocks: preserve learner code and explain how to refresh supplied tests.

### Task 1: Pybites contracts and test strength

Files: `cojudge/pybites/bites/b01.py` through `b22.py`, `cojudge/pybites/support.py`, `tests/test_pybites_course.py`, generated `cojudge/problems/pb-*`.

- [x] Add focused edge cases before reference fixes. Reproduce the b20 self-pairing defect.
- [x] Add `contract` and realistic `mutations` to each spec.
- [x] Show contracts before original descriptions and reject surviving mutations in verification.
- [x] Run all reference, template and mutation checks with the actual Python 3.11 runner.
- [x] Build all 22 native problems. Commit and push this unit (`355370d`).

### Task 2: Production Engineering Tickets

Files: `cojudge/production/`, `scripts/production_course.py`, `tests/test_production_course.py`, generated `cojudge/problems/pe-*`, `cojudge/courses/software-engineering/courseinfo.json`.

- [x] Write manually expected cases first for 24 tickets covering data, APIs, reliability, state, SQL, files, UTC, permissions, paths, versions, dependencies, synchronization, and HTML.
- [x] Add a small builder with named Python functions and a supplied adapter.
- [x] Verify references against manual expectations and independent Java implementations.
- [x] Reject realistic mutations and wrong output types; check repeated and reversed execution.
- [ ] Run the full repository test suite. Commit and push this unit.

### Task 3: Live publication

Files: live content only, plus deployment records in both repositories.

- [x] Back up affected course indexes and Pybites problems outside the public content directory.
- [ ] Stage new problems before publishing the new course index.
- [ ] Verify all references and representative faulty solutions through Run and Submit on the VPS. Do not write learner progress.
- [ ] Remove the three requested indexes by moving them to the backup directory.
- [ ] Confirm the new course has 24 complete problems and all 22 Pybites updates are present.
- [ ] Record verification and the rollback location. Commit and push documentation.

## Decisions and evidence

- The user asked for broad software engineering practice after the initial draft. Expanded from 16 to 24 tickets. Use `software-engineering` as the course ID.
- The User bite guarantees nonempty ASCII names. It does not require validation of excluded inputs.
- Preserve saved Pybites tabs. A new editor tab supplies the current tests; copy the learner implementation into that tab.
- Independent review found a hidden decimal precision assumption. Copied decimal values now have explicit bounds of six decimal places and absolute value at most 1000000. Added boundary cases and verified both implementations.
- Independent review found that input mutation was not observed by the judge adapter. A failing test reproduced it. The adapter now compares input snapshots and rejects changes. The test passes.
- The repository suite passed 85 tests. Pybites passed 390 cases and rejected 83 faults. The new tickets passed 380 manual cases and rejected 103 faults.
- A later shared-checkout run passed the same 85 tests but found four tests from concurrent, unfinished Pytest Path work: `test_empty_suite_cannot_pass`, `test_false_assertions_cannot_kill_mutants`, `test_weak_suite_leaves_mutants_alive`, and `test_reference_suites_pass_and_each_starter_fails`. All failed because `cojudge/pytest_path/support.py` was not implemented. Those files are outside this task and remain untouched. Verify this task again from a clean archive of its committed files.
- Before-publication backup: `/home/ubuntu/cojudge-backups/software-tickets.PJshjq/content-before.tar.gz`.
