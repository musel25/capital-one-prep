# Pybites Collections Path

**Goal:** Add the 11 exercises from the Collections Module path to the live Cojudge site.

**Scope:** Follow the existing Pybites OOP format. Use Python 3.11, the existing test runner, independent `pbc-` problem IDs, and course ID `pybites-collections`. Preserve exercise order. Reuse available free templates and tests. Label recreated premium exercises. Replace downloads with supplied offline data. Preserve existing learner work and unrelated working changes.

**Files:** `cojudge/collections_path/` holds captured public descriptions, exercise specifications, the builder, and its README. `scripts/collections_course.py` builds and verifies the course. `tests/test_collections_course.py` checks completeness and the judge contracts. Generated content goes in `cojudge/problems/pbc-*` and `cojudge/courses/pybites-collections/`.

- [x] Add tests that require all 11 exercise specifications, reject empty starters and plausible faulty solutions, and verify course order.
- [x] Add exercise specifications with input contracts, boundary tests, references, and local data. Reuse the established runner without changing the OOP course.
- [x] Verify all references and rejection checks with Python 3.11. Build all problem files. Review generated content and run the Cojudge CLI.
- [x] Commit only this course and push. Publish only its new directories. Verify correct and incorrect solutions on the live judge without calling the progress API. Check the course in the browser.

**Review focus:** empty inputs; ties and stable order; punctuation and aliases; CSV quoting and filtering; bounded queue state after append; HTML table selection; no network access; no writes to learner progress.

**Execution:** Continue in the existing checkout with additive paths. The checkout contains unrelated OOP edits. Do not stage or change those files. The user requested the same import workflow as the existing course.

**Local evidence:** 14 new tests pass. The combined Collections/OOP verifier tests pass (17 tests). The builder verifies 79 judge tests across 11 exercises. CLI init produces all 11 exact templates. Fresh review found one overly broad namedtuple field contract; it now excludes leading underscores and keywords. Review found no remaining material issues. The original movie data retains all 5,043 rows, projected to the four required fields. The cached holiday table matches its source.

**Publication, October 28, 2026:** Content from `836fc24` was staged at `/home/ubuntu/cojudge-staging/collections-836fc24/`. Every target directory was absent before publication. Only the 11 `pbc-*` problem directories and the new course directory were copied into the existing content volume. The course was copied last. No application restart or configuration change was needed. The browser shows all 11 titles in source order and progress `0 / 11`. Live submissions passed all 79 reference tests and rejected all 11 unfinished templates. CLI run also passed the queue reference and rejected its starter. The checks did not call the progress API.

**Recovery:** The staging folder retains the exact published files. To hide this course by default, set `hidden` to `true` in its courseinfo.json. Existing viewer choices in the Lists menu can still show it. Preserve problem directories and learner progress.
