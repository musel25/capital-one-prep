# Unfamiliar exercise sequence

The learner found days 1 and 2 repetitive because both expose the same Cedar
Wallet implementation. Audit: 14 of 20 tasks use that application. The planner
also explains likely fixes before the learner investigates.

The requested improvement is to practice clarification, codebase navigation,
hypothesis formation, tests, and review of AI changes against unfamiliar behavior.
Preserve existing learner attempts, private notes, task IDs, planner progress,
dates (October 23–November 1, 2026), and 225 minutes per day.

## Implementation decisions

- Preserve d01-bug, d01-feature, and the completed d02-bug. Every subsequent task
  uses a distinct application context, including each day's feature. Retain the
  previously unseen settlements/promotions/inventory bug apps for days 8–10.
- Add 14 small, substantive applications. Different domain data, module
  responsibilities, and business rules matter more than framework variety.
  Retain Python/FastAPI and the existing dependencies and uv workflow.
- Each app has one seeded bug or missing feature, usable browser/API context,
  public tests of existing behavior, and external checks that fail on the
  starter and pass on the reference. No source locations or fix recipes in
  learner briefs. Keep each task achievable within its existing time budget.
- Default new attempts to interview mode: symptom/request and neutral product
  context in README; exact behavior and example requests in CLARIFICATIONS.md.
  Learner writes questions first, then consults that file as interviewer answers.
  `--mode guided` exposes the same contract up front. This is practice scaffolding,
  not a claim about Capital One's exact format or a security boundary.
- Keep version-1 catalog, patches and checks available. Version-1 manifests
  continue to execute their old contract; new manifests select revision 2.
- Planner technical blocks describe products, workflow, and ownership of tests,
  without explaining seeded causes. Preserve nontechnical activities and timing.
- Do not open, rewrite, or create user attempts as part of maintenance. Exercise
  construction/verification uses temporary directories only. No instructor
  modules or reference implementations are copied into learner folders.

## Verification

Verify new applications through real TestClient requests. For every task, public
tests pass on starter and reference; external task checks fail by assertion on
starter and pass on reference. Check legacy-manifest routing and nonmutation,
distinct remaining contexts, mode behavior, no instructor leakage, and planner
alignment. Run Python and website suites and production build.
