# Pybites Datetimes and Timezones Path

Goal: Add all 24 exercises in the supplied order to the existing Cojudge site.

Use the established Pybites runner and authoring layout. Create course ID
`pybites-datetimes-timezones` and independent `pbd-` problem IDs. Retain the two
free exercises. Label the other 22 as recreated exercises. Supply fixed local
fixtures and standard-library replacements for dateutil. Keep exact input rules
in every statement. Do not change learner work or other courses.

- [ ] Check completeness, order, free source retention, and mutation rejection.
- [ ] Add specifications, reference solutions, test cases, builder, and CLI.
- [ ] Verify references, reject starters and faults, and build all 24 problems.
- [ ] Commit this course and push. Publish only its new directories.
- [ ] Verify reference and starter submissions through the real judge and CLI.
- [ ] Check the course list and problem editor in the browser.

Review: leap days; year boundaries; DST; ambiguous formats; duplicate and missing
dates; ties; empty inputs; stable time defaults; no network in learner code.

Execution: Use additive files in this checkout. Other course imports are in
progress in this checkout. Stage only the datetimes course files.
