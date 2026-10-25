# Unfamiliar Exercises Implementation Plan

> **For agentic workers:** Use independent application builders and integrate centrally; run real starter/reference checks before committing each coherent unit.

**Goal:** Replace repeated remaining tasks with unfamiliar projects and a clarification-first workflow while preserving old attempts.

**Architecture:** Keep revision-1 definitions available; merge revision-2 task metadata, patches and checks from scenario modules. Each template is self-contained. CLI chooses checks from the manifest revision.

**Tech Stack:** Python/FastAPI, pytest/TestClient, uv, React/Vite planner.

**Spec:** docs/superpowers/specs/2026-10-24-unfamiliar-exercises-design.md

## Global constraints

No edits to attempts/ or private/. No dependencies added. English learner content.
Keep task IDs, existing schedules, progress storage and total daily minutes.
Commit coherent units and push immediately after each commit.

## Review focus

- Old attempts with no revision field must still invoke their original checks.
- Task contracts and generated READMEs must match external behavior assertions.
- Passing public tests must not accidentally satisfy the assigned task.
- Every remaining context must be different in behavior and structure, not just names.
- Planner text must not expose causes or refer to replaced domains.

## Tasks

- [x] Build independent templates, task metadata, patches, external checks, and
  existing-behavior tests in three disjoint groups. Each group verifies references
  pass and starters fail for the intended assertion.
- [x] Add failing platform tests for revision dispatch, interview/guided modes,
  remaining context uniqueness, public test preservation, and malformed revisions.
  Implement CLI/catalog integration and compatibility; run the Python suite.
- [x] Rewrite technical planner content and maintenance docs, preserving IDs,
  phases, dates, and nontechnical content. Run web tests and build.
- [x] Run all starter/reference and public suites, review the diff independently,
  fix material findings, commit and push. Report concrete changes without spoilers.

## Execution evidence and decisions

- Initial Python suite: 24 passed; web suite: 15 passed.
- New platform tests first failed for repeated contexts, missing clarification
  sheet, schema-1 manifests and absent revision support; after implementation
  the targeted platform suite passed 20 tests.
- Application builders verified each new starter/reference pair in temporary
  directories. Root verification covers 20 current pairs and public suites;
  separate legacy verification covers all 20 original pairs.
- Independent reviewer inspected platform, middle/late apps and curriculum;
  primary agent reviewed early apps. Found year-zero months and maximum-date
  overflow; new assertions reproduced both, then passed after fixes.
- Final Python suite: 34 passed. Web suite: 15 passed. Production build passed.
- Decision: preserve Python/FastAPI and small applications rather than add setup
  variability. This develops unfamiliar-domain navigation, not framework breadth.
- Decision: separate exact contracts into a learner-accessible clarification
  sheet, with guided mode optional. This models questions without making a
  security boundary or pretending requirements can be guessed.
