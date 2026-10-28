# Pybites Datetimes and Timezones Path

Goal: Add all 24 exercises in the supplied order to the existing Cojudge site.

Use the established Pybites runner and authoring layout. Create course ID
`pybites-datetimes-timezones` and independent `pbd-` problem IDs. Retain the two
free exercises. Label the other 22 as recreated exercises. Supply fixed local
fixtures and standard-library replacements for dateutil. Keep exact input rules
in every statement. Do not change learner work or other courses.

- [x] Check completeness, order, free source retention, and mutation rejection.
- [x] Add specifications, reference solutions, test cases, builder, and CLI.
- [x] Verify references, reject starters and faults, and build all 24 problems.
- [x] Commit this course and push. Publish only its new directories.
- [x] Verify reference and starter submissions through the real judge and CLI.
- [x] Check the course list and problem editor in the browser.

Review: leap days; year boundaries; DST; ambiguous formats; duplicate and missing
dates; ties; empty inputs; stable time defaults; no network in learner code.

Execution: Use additive files in this checkout. Other course imports are in
progress in this checkout. Stage only the datetimes course files.


Verification and publication record, October 28, 2026:

- Course implementation commit: `73a2788`, pushed before publication.
- Seven new-course/OOP regression tests passed. The build verified all 174
  exercise tests, rejected all 24 starters, and detected all 51 deliberate faults.
- Independent review found malformed git-stat acceptance, year padding defects,
  and missing parser/error tests. These were fixed before the final build.
  The reviewer confirmed the fixes and found no remaining blocking issue.
- Published only the new `pbd-*` problem directories and
  `courses/pybites-datetimes-timezones` into the existing content volume.
  Every target path was absent before extraction. No application restart.
- Live judge: all 24 reference submissions accepted, totaling 174 test cases.
  All 24 starter submissions rejected.
- Actual Cojudge CLI: `init` produced the timezone starter; `run` passed all
  three samples; `submit` accepted its reference (7/7) and rejected its starter
  (0/7). The CLI used a temporary OS home and content directory. Its local
  solved flag was saved only in that temporary directory.
- Browser DOM: the live course showed all 24 ordered problem links, grouped as
  5 beginner, 17 intermediate, and 2 advanced. The timezone problem response was
  HTTP 200 and contained its Python template, offline timezone data, and tests.
  The authenticated browser showed the existing owner profile and Saved to VPS.
- Live verification submitted code directly. It did not call the progress API
  or replace learner files. Browser inspection opened the course list and read
  the problem response without opening a learner editor.
