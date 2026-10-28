# Pybites Data Formats Path Implementation Plan

**Goal:** Add the 17 requested exercises to the existing live Cojudge site in source order.

**Architecture:** Reuse the existing OOP Python 3.11 test runner. Add independent `pdf-` problem IDs and course ID `pybites-data-formats`. Keep source descriptions and available free tests. Clearly identify recreated premium templates and offline data changes.

**Spec:** The user's ordered Data Formats list and `cojudge/pybites/README.md`.

**Constraints:** Preserve learner solutions and unrelated changes. Use `uv run`. Publish only the new content directories. Do not write learner progress. Commit this course as one coherent unit and push immediately.

**Review focus:** JSON numeric conversions; CSV quotes and empty rows; namespaced XML; empty collections and stable ties; real SQLite queries; all RPS pair outcomes; no network needed by submissions.

- [x] Capture the 17 public exercise pages and available free templates/tests.
- [x] Add a failing course-completeness test. Add specifications in separate files for independent exercise groups. Verify references, starters, and deliberate faults with the actual runner.
- [x] Add the course builder and command. Reuse existing specifications for the three exercises shared with the Collections path without requiring its uncommitted files.
- [x] Build the course. Run the course tests and the repository suite. Review all generated files.
- [ ] Commit only this course and push. Publish only its new directories. Verify all references and starters on the live judge. Check the course in the browser and with the Cojudge CLI.

**Execution choice:** Use additive paths in the existing checkout. Separate agents own independent exercise specification files. The main agent owns integration, review, Git, and publication.

**Local verification:** 22 course tests pass. All 17 references pass 140 judge cases. Starters fail, and all 46 deliberate faults are detected. The Cojudge CLI initializes all 17 Python starters in temporary files. Independent review found and reproduced truncated movie CSV rows, empty pickle errors, and decimal precision loss. These cases are corrected and covered by tests. Free source tests are preserved with normalized line endings.

**Repository suite:** The full run completed with 142 passed and one unrelated failure: `tests/test_datetimes_course.py::test_verification_checks_every_reference_starter_and_fault`. Datetimes exercise 10 rejects `US/Arizona` as an unknown timezone. This import does not change that course. The final Data Formats check after review passes all 22 tests.
