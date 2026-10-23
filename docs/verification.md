# Initial release verification

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
