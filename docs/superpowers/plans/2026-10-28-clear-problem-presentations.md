# Clear custom problem presentations

The user approved original Pybites context and tasks, real input/output examples,
and brief missing input guarantees. Runtime and editor instructions belong in
separate help. Apply this to the nine active custom lists (135 problems).

- [x] Add shared presentation helpers and actual test-code descriptions.
- [x] Restore original descriptions and verify all 244 displayed examples.
- [x] Refresh only statements, examples, check descriptions, and course help.
- [x] Preserve starter code, test cases, markers, references, and runtime libraries.
- [x] Show actual checks in CoJudge while preserving input editing and added cases.
- [x] Reproduce and fix the added-case editing regression found in review.
- [x] Add readable descriptions for later official checks as well as examples.
- [x] Run final checks and commit/push each repository's changes.
- [x] Back up live metadata and statements, then publish only presentation fields.
- [x] Build an isolated application candidate and verify that the current combined release includes the display change.
- [x] Verify all live statements and representative rendered pages without writing learner data.

The existing code, progress data, course indexes, and grading behavior stay in place.
The source refresh command fingerprints all judge data before and after each update.
The live installer must also preserve current metadata fields outside presentation.

Final evidence is in `cojudge/presentation-verification.md`. The current combined
release already includes this feature, so the isolated candidate was not activated
over newer UI changes. All 135 statements and 244 examples match the live server.
