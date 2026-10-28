# SQLModel path implementation plan

**Goal:** Add the ten SQLModel exercises to the existing Cojudge site, in the supplied order.

**Scope:** Use the same course format as the OOP import. All ten original exercises are premium. Label each recreation. Use real SQLModel, SQLite, FastAPI, HTTPX, and pytest. Keep learner solutions and progress unchanged. Use additive paths in the existing content repository. Do not include concurrent course work in commits.

**Files:** `cojudge/sqlmodel_path/` holds public descriptions, ten specifications, an isolated uv project, runner, builder, runtime Dockerfile, and instructions. `scripts/sqlmodel_course.py` builds and verifies content. `tests/test_sqlmodel_course.py` checks course order, reference solutions, incomplete starters, and faulty implementations. Output uses `pbs-` IDs and course `pybites-sqlmodel`.

- [x] Write checks for ten exercises, independent database state, durable commits, relationship isolation, validation, API errors, filtering, and real test failures.
- [x] Add templates, tests, reference solutions, and faults. Supply prior-stage code in later exercises.
- [x] Verify each reference passes. Verify each starter and fault fails. Generate all native problem files. Run the CLI starter check.
- [x] Build a locked Python runtime. Preserve the current stock image under a backup tag. The deployed judge uses the fixed `python:3.11-slim` tag, so point that local tag at the tested runtime. Record this deployment requirement and rollback steps. Do not replace active execution containers.
- [x] Publish only this course. Check references and starters through the live judge without writing progress. Check the live course page. Commit and push each complete unit.

**Review focus:** model registries must be isolated between tests and submissions; writes must survive a fresh session; joins must filter the exact workout/exercise pair; API validation and missing IDs must return correct status codes; each test run must use fresh temporary files.
