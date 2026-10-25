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

- [x] Test preserved archived notes, uncompleted replacement assignment, working problem links, staged case disclosure and shuffled question follow-ups.
- [x] Add accessible UI using existing styling; replace daily Python blocks with official LeetCode links and learning guidance, no local starter prompts.
- [x] Add an original virtual-card case with independently checked answer key. Improve business follow-ups, practical design and behavioral rehearsal.
- [x] Run npm test and npm run build; inspect desktop and mobile rendering.
- [x] Commit and push curriculum/UI unit.

### Task 2: Larger agentic mocks

**Files:** exercises/templates/support_ops/; exercises/templates/dispatch/; exercises/scenarios/mocks.py; exercises/coach/mocks.py; exercises/catalog.py; exercises/coach/starters.py; exercises/coach/run.py; tests/test_exercises.py; curriculum/plan.json; exercises/README.md.

**Interfaces:** Four new IDs mock-support-bug/feature and mock-dispatch-bug/feature, using existing revision-2 manifest, Task and check/build contracts. Existing 20 IDs and all previous revisions remain valid.

- [x] Write behavioral contract checks and no-overwrite/legacy compatibility tests; observe missing mock IDs fail.
- [x] Implement two meaningful multi-module apps, independent seeded faults/features, public existing-behavior tests and instructor checks.
- [x] Connect fresh late-session blocks to mock IDs; preserve old blocks in archive.
- [x] Run uv run pytest (includes starter/reference/public verification) and npm test/build.
- [x] Commit and push mock unit.

### Task 3: Review and publish

- [x] Fresh reviewer checks the complete diff, evidence, answer keys, contracts and progress preservation.
- [x] Fix material findings, verify affected behavior and complete suites.
- [x] Fast-forward the original checkout, push main, and deploy built static assets from the clean worktree using scripts/deploy.sh.
- [x] Verify live asset contents, current-day links, archive and mobile layout. Report actual delivery and limitations.

## Execution record

- Worktree: .worktrees/practice-upgrade; baseline f65039a.
- The user approved the proposed direction and explicitly requested website adaptation; implementation proceeds without another approval cycle.

- Task 1 completed in b23aa77 and pushed to origin/feat/practice-upgrade. New UI tests were observed failing before implementation, then passed.
- Task 2 adds four independent mock snapshots to the existing revision-2 catalog; missing-ID tests failed before implementation. Original 20 tasks and legacy revision-1 support remain.
- Final review found the day-9 required-work mismatch and altered archived mock definitions. Day 9 now requires two chosen attempts. The archived blocks were restored exactly from f65039a; the archive regression failed first and now passes.
- Strengthened the external checker after four deliberately incorrect implementations were incorrectly accepted: assignment history details, quote breakdown, cancellation event items, and rejected-shipment history. Each regression now fails the incorrect implementation with an assertion rather than a setup error.
- Browser checks: 1440px planner and 390px task modal/archive; official problem link, staged disclosure, behavioral draws/follow-ups and mock commands. Generated reference apps exercised queue/assignment/comment and quote/cancellation flows. No horizontal overflow; mock apps have only a harmless missing favicon request.
- Review scope: live publication and external-source validity were not judged by the reviewer. Browser checks cover rendering; publication is the next step. External sources were researched during curriculum design and are labeled by provenance.
- Build passes with Vite's bundle-size advisory (about 646 kB minified / 170 kB gzip). No dependency migration.
- Final verification before publication: 42 Python tests passed (including all 24 starter/reference/public pairs), 20 website tests passed, production build passed, and git diff --check passed. No deferred review findings remain.
- Mock/review unit committed as 8ea5e17, pushed, and fast-forwarded into main. scripts/deploy.sh published release 8ea5e176c371-20261025T195909; nginx and both existing application health checks passed.
- Live browser verified October 25 selection, the official Parking System link, both Support Ops commands, archived 90-minute definitions, no mobile horizontal overflow and no console errors. Published JavaScript is index-BFynP8bF.js. This final record-only commit does not change the deployed assets.
