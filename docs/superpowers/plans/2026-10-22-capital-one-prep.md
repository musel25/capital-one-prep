# Capital One Prep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Deliver a working daily preparation page and runnable local exercises for ten four-hour days.
**Architecture:** Static React planner consumes a versioned JSON curriculum. Python CLI makes isolated attempts from tested exercise templates. Browser progress remains private and exportable.
**Tech Stack:** React, TypeScript, Vite, Node test runner, Python/uv, pytest, FastAPI.
**Spec:** docs/superpowers/specs/2026-10-22-capital-one-prep-design.md

## Global Constraints
- October 23 through November 1, 2026 inclusive, each exactly 240 scheduled minutes in America/Tijuana.
- Spanish guidance, English interview prompts.
- Use uv for Python. Preserve learner attempts and private notes. Never publish them.
- No automatic carry-over or spaced repetition. Completion is self-reported, not proof of readiness.
- All commits immediately pushed. Root orchestrator owns Git and deployment; agents own disjoint files.

## Review Focus
- Before/after sprint and midnight timezone behavior: clamp selected day, label actual state.
- Corrupt or unknown imported data: validate before replacing existing progress, provide recovery/export.
- Repeated lab starts and unsafe identifiers: unique paths; no overwrite, traversal or instructor leakage.
- Case solutions and mocks: prediction recorded before solution reveal; no answer keys in learner workspace.
- Mobile/keyboard/refresh: reachable task controls, accessible modal, persisted notes/timer/progress.

### Task 1: Detailed curriculum
Files: curriculum/plan.json, cases/, behavioral/. Consumes twenty lab IDs d01-bug..d10-feature. Produces schema in spec.
- [x] Author all 10 days and complete prompts/cases/behavioral exercises, exact 240 minutes/day.
- [x] Include original variant cases, hidden answer keys, precise requirements and source labels.
- [x] Validate with content tests in Task 3 and resolve mismatches.
- [x] Commit and push coherent curriculum deliverable.

### Task 2: Runnable practice labs
Files: exercises/, scripts/practice.py, tests/test_exercises.py, pyproject.toml, uv.lock.
Interfaces: `uv run python scripts/practice.py list`; `start TASK_ID` returns unique attempt path; `check ATTEMPT_PATH` runs held-out tests and reports evidence without modifying attempt.
- [x] Test preservation on repeated starts, invalid IDs, no coach material in learner folders; observe RED.
- [x] Implement multi-file app templates, 20 independent starter tasks and instructor reference fixes.
- [x] Verify reference solution passes while targeted bug or missing feature fails for every task.
- [x] Verify local uv commands and document per-attempt startup in generated README.
- [x] Commit and push runnable labs.

### Task 3: Daily planner
Files: package.json, web/, tests/model.test.ts, tsconfig.json, vite.config.ts.
Interfaces: consumes plan JSON; model exports date selection, state validation, persistence helpers; app uses tasks by stable id.
- [x] Write model tests for date bounds, exact totals, import corruption and persistence; observe RED.
- [x] Implement models and React interface with daily agenda, detail panel, checklists, notes, saved predictions, hidden solutions, phase timers, export/import.
- [x] Run tests and production build; inspect accessible desktop/mobile UI when supported.
- [x] Commit and push planner.

### Task 4: Integrate, review and publish
Files: scripts/deploy.sh, README.md, docs/usage.md.
- [x] Validate all content links/lab IDs and all intended exercise failure/pass pairs.
- [x] Independent review; fix material findings and rerun affected checks.
- [x] Deploy immutable static release at /grind/capital-one/ with config backup and rollback; verify existing /grind/ and /api/health.
- [x] Save local launchers and explain how to begin tomorrow and ask for attempt review.
- [x] Commit and push deployment/docs; verify clean tracked state.

## Completion evidence

Implemented and published on October 22, 2026 (Tijuana). See [verification record](../../verification.md). Automated component tests cover the interaction flows; a real-browser visual inspection could not run because the browser tool exposed no available browsers.
