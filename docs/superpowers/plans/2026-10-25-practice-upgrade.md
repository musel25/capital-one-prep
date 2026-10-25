# TDP practice upgrade implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publish the approved preparation improvements in the existing website and runnable exercises.

**Architecture:** Keep the React planner, browser-local progress and Python/FastAPI exercise runner. Add explicit LeetCode links, staged case prompts and a shuffled behavioral rehearsal; add two larger original mock applications with separate bug and feature snapshots. Archive replaced blocks with their original content and retain all old exercise contracts.

**Tech Stack:** React/TypeScript, Vite, Python, FastAPI, pytest, uv.

**Spec:** User-approved recommendations in this conversation, October 25, 2026: daily LeetCode instead of standalone Python drills, stronger agentic/case/behavioral preparation, adapt and publish the website.

## Global constraints

- October 23–November 1, 2026; 225 minutes/day; America/Tijuana; English learner content.
- No writes to existing attempts or private behavioral notes. New attempts never overwrite work.
- Original exercises are labeled constructed practice; source testimony is not an official rubric.
- New LeetCode blocks get new IDs. Old blocks remain accessible with saved notes; backups remain compatible.
- Days 1–2 keep their existing non-Python content/timing. Remaining days use 75/60/30/60 minutes.
- No framework/dependency migration. Commit coherent units and push after each commit.

## Review focus

- Old completed Python work must not mark a new LeetCode assignment completed.
- Archived case predictions/solutions must not unlock a replacement case.
- New agentic starters must fail behavior checks, while their public tests still pass.
- Rejecting a multi-record operation must not partially mutate state or append history.
- Fresh feature and bug attempts must be independent, with no coach/reference code copied in.

### Task 1: Website curriculum and practice interactions

**Files:** curriculum/plan.json; web/types.ts; web/App.tsx; web/TaskDialog.tsx; web/styles.css; tests/interface.test.ts; tests/curriculum.test.ts; cases/; behavioral/question-bank.md; README.md.

**Interfaces:** Optional Block.problems, Block.stages and Plan.archivedBlocks; retain all existing Progress fields and storage key.

- [ ] Test preserved archived notes, uncompleted replacement assignment, working problem links, staged case disclosure and shuffled question follow-ups.
- [ ] Add accessible UI using existing styling; replace daily Python blocks with official LeetCode links and learning guidance, no local starter prompts.
- [ ] Add an original virtual-card case with independently checked answer key. Improve business follow-ups, practical design and behavioral rehearsal.
- [ ] Run npm test and npm run build; inspect desktop and mobile rendering.
- [ ] Commit and push curriculum/UI unit.

### Task 2: Larger agentic mocks

**Files:** exercises/templates/support_ops/; exercises/templates/dispatch/; exercises/scenarios/mocks.py; exercises/coach/mocks.py; exercises/catalog.py; exercises/coach/starters.py; exercises/coach/run.py; tests/test_exercises.py; curriculum/plan.json; exercises/README.md.

**Interfaces:** Four new IDs mock-support-bug/feature and mock-dispatch-bug/feature, using existing revision-2 manifest, Task and check/build contracts. Existing 20 IDs and all previous revisions remain valid.

- [ ] Write behavioral contract checks and no-overwrite/legacy compatibility tests; observe missing mock IDs fail.
- [ ] Implement two meaningful multi-module apps, independent seeded faults/features, public existing-behavior tests and instructor checks.
- [ ] Connect fresh late-session blocks to mock IDs; preserve old blocks in archive.
- [ ] Run uv run pytest (includes starter/reference/public verification) and npm test/build.
- [ ] Commit and push mock unit.

### Task 3: Review and publish

- [ ] Fresh reviewer checks the complete diff, evidence, answer keys, contracts and progress preservation.
- [ ] Fix material findings, verify affected behavior and complete suites.
- [ ] Fast-forward the original checkout, push main, and deploy built static assets from the clean worktree using scripts/deploy.sh.
- [ ] Verify live asset contents, current-day links, archive and mobile layout. Report actual delivery and limitations.

## Execution record

- Worktree: .worktrees/practice-upgrade; baseline f65039a.
- The user approved the proposed direction and explicitly requested website adaptation; implementation proceeds without another approval cycle.
