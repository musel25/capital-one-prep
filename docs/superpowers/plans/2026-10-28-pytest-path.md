# Pytest Path Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan.

**Goal:** Add the ten Pybites Pytest path exercises to the existing private CoJudge deployment.

**Architecture:** Follow the existing `cojudge/pybites` content generator. A supplied standard-library runner executes learner tests against the correct module and explicit faulty variants. Exercise 1 uses the visible original code. Exercises 2–10 are labeled offline recreations from the public descriptions.

**Tech Stack:** Python 3.11 in the judge, uv, JSON course content, Java marker.

**Spec:** The user's ordered list and the existing OOP course in `cojudge/pybites/README.md`.

## Global Constraints

- Preserve existing learner progress and unrelated uncommitted files.
- Keep the ten exercises in their source order.
- Learners write tests, not implementations.
- Do not claim pytest-cov or mutatest parity. Explain the supported pytest subset.
- Use `uv run` for Python commands. Push each commit immediately.

## Review Focus

- Reject empty suites and suites that already fail against correct code.
- Report a surviving fault instead of accepting weak tests.
- Restore fixtures, patches, streams, and modules between runs.
- Reject collection failures and missing test targets.
- Verify reference and starter submissions through the deployed judge.

## Task 1: Course content and test-writing runner

- [x] Read the original path pages and OOP course generator.
- [x] Write and run failing checks for empty, invalid, and weak suites.
- [x] Add `cojudge/pytest_path/{support,runner,specs}.py` and a CLI script.
- [x] Define ten targets, reference tests, contracts, and fault variants.
- [x] Run all reference suites against correct and faulty targets.
- [x] Build all ten native problem folders and the ordered course list.
- [x] Run the repository test suite.
- [x] Commit only this course and push.

## Task 2: Publish and verify

- [x] Copy only the new course and problems to the existing content volume.
- [x] Submit each reference and starter through the deployed judge.
- [x] Confirm that the browser shows all ten exercises.
- [x] Record the verification and course link.

## Verification record

All 9 runner regression tests pass. All ten references pass 67 local checks, detect 57 faults, and also pass under real pytest. All ten reference submissions pass on the live judge; all ten starters are rejected. The CLI and browser show all ten exercises. Independent review found and confirmed fixes for patch decorators and shared built-in fixtures.

The later repository-wide run has 109 passing tests and 24 failures in unrelated, unfinished data-formats and SQLModel builders. A prior run stopped on the missing datetimes builder during its creation. Preserve that work. The earlier complete suite passed 106 tests. See the course README for the publication record.
