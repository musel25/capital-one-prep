# Clear problem presentation — October 28, 2026

Published the approved format across nine custom lists and 135 problems.

- Original Pybites context and tasks are visible.
- 244 examples use real Python calls, requests, or commands and expected results.
- 1047 supplied checks have readable code descriptions. The testing course shows the target or faulty implementation under test.
- Runtime, editor, migration, and source notes are in optional Course help.
- Software Engineering Tickets use short context, direct tasks, named calls, and concise input bounds.

Verification:

- All 165 Python repository tests pass. Example tests execute every displayed example against its reference.
- The presentation refresh fingerprints all execution metadata, official tests, markers, references, and bundled libraries before and after each change. They are unchanged.
- CoJudge passes 275 unit tests, its production build, and three focused browser tests. Type checking retains the existing baseline of 30 errors and 29 warnings; no new errors were introduced.
- Independent review found an added-case editing regression. A new browser test failed first. The correction keeps added cases editable and provides an explicit edit action for named checks. The test now passes.
- A later-check test failed first for Date and Data Formats checks beyond the initial examples. All official selectors now have readable descriptions.
- All 135 statements, 244 examples, 1047 check descriptions, help sections, and unchanged judge metadata match the published server responses.
- Reference sample runs pass for every list: 26 live checks across nine courses.
- Live browser checks confirm the original Vehicles task, literal output placeholders, real examples, actual Motorbike assertions, editable added cases, and closed help. Progress writes were blocked in the isolated browser checks.

Content commit: `03904a9` in `capital-one-prep`.
Application feature commit: `968acc8` in `cojudge`.
The current combined application image is `cojudge:no-legend-1b3fbdf`; it includes
the presentation feature and the later home-page cleanup. The isolated
`cojudge:clarity-968acc8` candidate was built but was not activated over the newer release.

Backups are outside the served content directory:
`/home/ubuntu/cojudge-backups/clear-problems.GZZUeb/originals/<problem-id>/`.
Each problem has its prior `metadata.json` and `statement.md`. The installer checked
all live starter hashes, test inputs, function metadata, and official tests before
publication. It then replaced only presentation fields and statements with atomic
file writes. `published.json` records the affected IDs and publication time.

Learner solutions, progress, course indexes, dependencies, and grading files were
not changed. To reverse the text update, restore the prior statement and presentation
fields from these backups. Keep current execution fields and learner data in place.
