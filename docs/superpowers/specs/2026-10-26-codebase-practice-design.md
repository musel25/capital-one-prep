# Codebase practice with independent AI review

## Intent

Replace the main technical recommendation with progressive practice in reading,
testing, and changing existing code. The learner already knows basic LeetCode.
They want detailed, bounded tasks and stronger technical judgment when using AI.
They will write implementations and tests. AI is an explanation and review tool.
There is no fixed problem-count target and no promise of interview readiness.
SQL is optional enrichment, not a prerequisite inferred from the TDP posting.

## Format and scope

Builder choice, open to user correction: 16 CoJudge repair exercises plus eight
short local repository labs. CoJudge checks function behavior. Local labs teach
real pytest, imports, file navigation, dependency replacement, and API tests.
Do not claim an output judge measures code navigation or test quality.

Publish a new native course, `capital-one-codebase-practice`, on the authorized
CoJudge website. Its description and statements link to a public repository
guide with the full sequence and local start commands. Native problem IDs start
with `cb-`, so old completion marks cannot imply completion of new exercises.
Keep the earlier 50 problems available as optional extended practice. Keep all
existing learner attempts and private notes untouched. The existing dated
planner remains compatible; this revision replaces the technical course entry.

Use Python 3.11-compatible code on CoJudge. Local labs use the repository's
Python >=3.12 environment with uv, pytest, FastAPI, and httpx. Do not add packages
unless a real requirement needs them. Use deterministic data, fake clocks, and
fake transport clients. There are no real network calls or live credentials.

## Browser sequence

Reuse the verified behavior contracts and independent Java oracles where they
fit. Rewrite the learner experience: every starter is an existing runnable
implementation with a disclosed defect. Every task explains its entry point,
data flow, allowed edit scope, compatibility requirements, and test strategy.
Do not merely rename the old course. Record the source problem for provenance.

| New number | Existing contract | Main learning objective |
| --- | --- | --- |
| 01 | p03 | Trace defaults and distinguish absent, null, and zero |
| 02 | p07 | Read typed boundaries and reject invalid runtime values |
| 03 | p11 | Trace instance state and repair shared mutable data |
| 04 | p12 | Track ownership through nested copies |
| 05 | p14 | Follow inherited methods and overridden behavior |
| 06 | p15 | Follow a composed dependency through a Protocol |
| 07 | p16 | Find state transitions and preserve rejected-operation behavior |
| 08 | p17 | Locate commit boundaries and prevent partial writes |
| 09 | p21 | Trace route and method dispatch |
| 10 | p22 | Validate an API body before side effects |
| 11 | p23 | Preserve PATCH compatibility and field presence |
| 12 | p24 | Trace replayed requests and conflicting identities |
| 13 | p25 | Write boundary cases for pagination order |
| 14 | p26 | Read error classification and retry policy |
| 15 | p27 | Follow a shared timeout budget |
| 16 | p30 | Check a client integration across several helpers |

Four levels contain four browser exercises each. Insert two local labs after
each level. The final guide presents this as one ordered sequence of 24 tasks.
The count is a builder choice based on distinct skills, not a completion target.

Every browser statement includes:

1. A short orientation and one learning objective.
2. A concept lesson with a small worked trace, before the task.
3. Named code regions to inspect, without naming the defective expression.
4. Exact input/output and error contracts from the verified source problem.
5. One scoped repair, explicit non-goals, and compatibility checks.
6. Specific test classes and at least one prediction to make before Run.
7. One optional AI prompt that requests evidence and forbids implementation.
8. One supplied AI claim to verify, with its answer in the optional solution.
9. A done checklist that separates judge evidence from manual code review.
10. Links to the next task, the course guide, and the relevant local lab.

Reuse all existing distinct official cases. Add independently derived cases for
new uncovered boundaries. Verify that each runnable starter fails a behavior
assertion, every reference passes, and all prepared faulty variants are rejected.
Preserve output-type checks and independent Java computations for custom inputs.

## Local labs

Use three compact constructed codebases: configuration/intake, a ticket API,
and a paged client. Each has 3–6 small application files. Public tests demonstrate
supported behavior but do not solve the assignment. Each lab starts from an
independent snapshot with earlier requirements already implemented.

| ID | Task | Evidence required |
| --- | --- | --- |
| lab01 | Map an intake pipeline and write characterization tests | Tests cover entry point, transformation, and a rejection path |
| lab02 | Parameterize boundary tests for a typed input validator | Correct implementation passes; faulty validators fail |
| lab03 | Reproduce and fix state leakage between instances | Failing regression before the fix; isolation after the fix |
| lab04 | Replace a dependency with a fake and test exception behavior | Test the caller; preserve real logic under test |
| lab05 | Trace an HTTP request and fix validation before writes | Status, response, and unchanged state on rejection |
| lab06 | Add a small PATCH field and preserve existing semantics | Missing/null/zero and compatibility integration tests |
| lab07 | Test a retrying client with fake transport and clock | Exact calls, budgets, stop conditions; no sleep or network |
| lab08 | Review a plausible AI patch and repair one regression | Independent reproduction, own tests, small diff, full suite |

Each brief is self-contained. Give the product rule, relevant file map, exact
editable files, startup and focused-test commands, accepted behavior, examples,
edge-case checklist, staged hints, and technical completion evidence. Teach
pytest assert/raises/parametrize/fixtures, fake dependencies, patch lookup scope,
unit versus integration checks, test isolation, and the limits of coverage.
Include practical rg, pytest collection, traceback reading, and git diff usage.
No behavioral-interview or spoken-presentation deliverables.

The learner writes tests. Never tell them to ask AI to write the first regression
or to implement the feature. AI prompts request a code path with file evidence,
questions about an assumption, or review of a learner-written diff. Supplied AI
claims are constructed examples, not real model outputs or employer material.

## Local runner

Add a separate `scripts/codebase.py` command with list/start/check/verify.
Default attempts go into new unique directories under attempts. Start never
overwrites. Check copies the selected attempt into a temporary directory and
never modifies it. Reject unexpected symlinks and traversal in manifests.
Keep instructor references, contract tests, and faulty variants outside attempts.

For test-focused labs, run learner tests against a correct implementation and
several disclosed classes of faulty implementations. A correct implementation
must pass. Each faulty implementation must cause an assertion failure, not an
import, collection, or setup error. Require at least one actual collected test.
For repair/feature labs, run learner tests plus separate behavior checks on their
implementation. Also check that their regression test detects the seeded defect
where the lab contract requires it. Do not infer code quality from a pass count.

Return exit 0 for sampled success, 1 for unmet behavior or test evidence, and 2
for setup/execution errors. The tool is a local training checker, not a sandbox.

## Verification and publication

Complete the already running supplemental verification for the original course
as a separate coherent unit. Preserve its evidence independently from this revision.
For the new work, verify browser starters/references, Java agreement, manual cases,
and mutations locally. Check local lab starter/reference pairs and sample learner
test suites, including empty tests and infrastructure failures. Run repository
regressions. Publish new problem files first, run every new problem through live
Run and Submit, then publish the course index. Verify the published hashes and
ordered server course data. Do not claim browser UI testing if unavailable.

Commit each coherent unit with Conventional Commits. Push each commit immediately.
The user authorized the revision and publication. They said to redo the curriculum
and delegated its length; do not request another approval for routine content work.
