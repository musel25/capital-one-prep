# Curriculum and checker review

The revised course was reviewed on October 26, 2026. The design received an
independent builder check before implementation. The check found no material
unanswered requirements. Authors worked on separate browser and local-lab files.

The browser author checked 40 hand-derived cases for the worked traces and AI
claim answers. Those expectations are saved in `lesson-review-cases.json`.
They were then checked against both Python references and independent Java
oracles. The earlier independent cases remain separate from generated inputs.

The local authors checked correct source, public tests, independent contract
tests, sample learner tests, and realistic faulty variants in temporary folders.
The shared runner also verified all eight sample completed attempts. It accepted
69 sample learner tests and rejected 28 faulty variants through assertions.

## Findings and corrections

An independent code review found two material issues:

1. Copied prerequisites referred to the old 50-problem sequence. The new builder
   now assigns explicit prerequisites from the new sequence. All 16 statements
   were rebuilt and checked.
2. The checker searched failure messages for the substring `AssertionError`.
   A faulty function raising `RuntimeError("AssertionError in adapter")` could
   pass that check. A regression test reproduced the false result. The checker
   now accepts strict pytest assertion-message forms. The regression passes.

The runner tests also cover empty tests, skipped tests, weak tests, collection
errors, ordinary crashes, attempt preservation, protected files, manifests, and
symlinks. All eight lab verification runs passed again after the checker fix.
The repository suite passed 77 tests. No frontend code changed in this revision.

The review found no further material contract mismatch in the eight labs. It
confirmed that the lesson code paths use actual symbols and that the AI prompts
request explanation or review rather than delegated implementation.

## Limits

This is a local training checker for learner-owned code. It is not a hostile-code
sandbox. Finite cases and prepared faulty variants do not prove that all possible
defects are detected. The browser judge checks behavior; it cannot measure code
navigation, annotations, architecture, or the learner's reasoning. Live endpoint
and publication results are recorded separately in the verification report.
