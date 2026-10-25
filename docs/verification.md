# Verification history

## October 24, 2026 — unfamiliar application sequence

The revised catalog keeps the three initial Cedar Wallet tasks and uses 17
distinct applications for the remaining 17 tasks. Fourteen new reference apps
were added; all remaining tasks include public tests of existing behavior.
New attempts support interview/guided modes. Existing schema-1 attempts retain
their original checker and are never migrated or rewritten.

Verification for this update:

- `uv run pytest -q`: 34 passed, including all 20 current starter/reference
  pairs, their public suites, mode generation, revision validation, old-attempt
  compatibility, preservation of learner files and instructor separation.
- `uv run python scripts/practice.py verify --revision 1 --json`: all 20 old
  starters failed by behavior assertion, all 20 old references passed, and their
  original public startup suites passed on both versions.
- `npm test`: 15 passed. `npm run build`: successful; the existing Vite chunk-size
  advisory remains (about 153.5 kB compressed main JavaScript).
- Independent review reproduced unintended year-zero validation and maximum-date
  overflow in new references. Added coach assertions failed before the changes
  and passed after calendar-month validation and overflow-safe report calculation.
- A data comparison against the prior commit confirmed unchanged dates, block
  IDs, lab IDs, time budgets, timer phases and all nontechnical activities.
- Browser checks exercised the four early app workflows and the updated day-two
  planner modal without page errors. Other new UIs have HTTP asset and JavaScript
  syntax checks; they have not all received a visual browser review.

These remain small, constructed Python/FastAPI exercises. Distinct domains and
module responsibilities increase navigation practice; they do not establish an
exact match for an employer's repository size, prompt or AI-use policy.

## Initial release — October 22, 2026

Recorded October 22, 2026, America/Tijuana. Published code: `f95bcf6f2c73`.

- `npm test`: 10 passed. Covers all ten calendar days and 240-minute totals, source/lab references, date boundaries, progress validation, case-review gating, timer and notes restoration, corrupt imports, cross-tab write protection, and preservation of unsaved notes when storage fails.
- `npm run build`: TypeScript and Vite production build passed. Vite reports a bundle-size advisory; the main JavaScript payload is approximately 167 kB compressed.
- `uv run pytest -q`: 24 passed. Includes all 20 original starter/reference behavior pairs, path validation, preservation of attempts, checker error handling, pinned upstream file hashes and Gilded Rose requirements.
- Each of the 20 original starter tasks fails its target contract; each corresponding instructor reference passes. Startup smoke checks alone are explicitly distinguished from task completion.
- Gilded Rose's unchanged upstream file passes existing behavior checks and fails the absent extension. The local reference passes 31/31 checks; the upstream snapshot has eight expected extension failures. The original MIT license is retained.
- Independent review inspected the implementation, exercise contracts, case solutions, provenance and deployment. One reproduced note-loss issue was corrected and independently rechecked; no material findings remained.
- Deployment health checks passed. The live HTML, JavaScript, stylesheet and favicon match the local production build byte-for-byte/SHA-256. The existing `/grind/` page returns HTTP 200 and `/api/health` reports `ok: true`; its release symlink remains unchanged.
- Git excludes learner attempts and private notes. Deployment uploads only `dist/`.

The interface interaction checks use JSDOM. They do not establish visual layout or real-browser compatibility: the available computer-use tool returned no browsers, so desktop/mobile screenshot inspection was unavailable. A successful build and passing checks are evidence about this training workspace, not a guarantee of interview readiness or confirmation of interview tool permissions.

The release initially needed privileged creation of its own static directories. A subsequent HTTP check reached an old Nginx worker immediately after graceful reload; rollback restored the prior configuration. The script now prepares directories with the deployment user's ownership and retries the new route during worker replacement. The final release passed its checks without changing the previous Grind Recall release.

## Tutorial and pre-start recheck

The requested website overview adds a persistent **Empieza aquí** link and a direct `?view=guide` URL. It explains the page/editor/review workflow, independent attempts, phase timers, case predictions, behavioral practice and private backups.

Fresh checks passed: 24 Python tests, 11 frontend tests and the production build. The added navigation test verifies that opening the tutorial, returning to day one and reloading preserve existing saved practice. Independent review found no material issues in the tutorial or navigation.

A temporary day-one attempt was created through the CLI. Its `uv venv`, `uv sync --frozen`, startup tests and actual Uvicorn server all succeeded. HTTP checks reached the app, documentation, transaction endpoint and JavaScript asset. The unchanged starter returned the expected unmet-contract result. The temporary server and workspace were removed; existing learner attempts were untouched. Real-browser visual inspection remained unavailable because the computer-use tool returned no browsers.
