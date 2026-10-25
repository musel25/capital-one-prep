# Capital One Prep

A ten-day preparation workspace for Capital One TDP Mexico, October 23–November 1, 2026. Three hours and forty-five minutes each day: AI-assisted debugging and feature work, technical business cases, behavioral practice, and targeted Python exercises.

The daily page provides the agenda. Code is practiced in your own editor, with independent attempt folders that preserve your work. The website and interview exercises are in English.

**Open the planner:** [timer.musel.dev/grind/capital-one/](https://timer.musel.dev/grind/capital-one/)

## Start practicing

```bash
cd /home/musel/Github/capital-one-prep
uv sync
uv run python scripts/practice.py start d01-bug
```

Open the newly printed directory in your editor and read its README. It includes the startup commands and the exact task. Run `start` again for a fresh attempt; it never overwrites previous work. To check a solution, run `uv run python scripts/practice.py check attempts/YOUR-ATTEMPT` from the repository root.

Starting with **d02-feature**, every remaining task uses a different application,
including the bug and feature on the same day. The sequence includes support,
shipping, scheduling, reporting, telemetry and other domains. Existing attempts
keep their original code and checks. Open an existing folder to resume it; run
`start` to get the revised exercise.

New attempts default to **interview mode**: read the symptom or request, write
your clarification questions, then consult `CLARIFICATIONS.md` for acceptance
criteria. Use `start TASK_ID --mode guided` to show the contract up front.
Describe a regression test yourself, let AI implement it if useful, review it,
and observe it fail before changing the application.

The schedule has 40 blocks across ten days. Python practice now links directly to daily LeetCode assignments: Two Sum, Valid Anagram, Parking System, Simple Bank System, Ordered Stream, Underground System, Recent Calls, Group Anagrams, Log Files, then an independent Bank retry. From October 25, the daily allocation is 75 minutes agentic practice, 60 case, 30 behavioral and 60 LeetCode. Days 1–2 keep their earlier timing.

Cases reveal business discussion, rules, code and follow-ups in stages; answer keys remain gated by a saved prediction and finished attempt. Behavioral rehearsal draws questions without repetition and reveals follow-ups after the initial answer. Stage/question position is session-only; save it in Notes to resume. Replaced exercises and their saved notes are available under **Previous exercises** and remain in backups, without counting toward the new assignments. New LeetCode blocks never inherit old completion marks. There is no separate closing block.

The 20 application tasks are **original training exercises**. Day 9 also uses a real, unmodified Python snapshot from [Gilded Rose](external/README.md), pinned to an upstream commit with its MIT license. Sources distinguish official platform documentation, candidate accounts, and constructed practice. None confirms your specific interview's tool permissions or timing.

Progress stays in this browser. Export a backup into `private/` when you finish a day; import it to continue on another device. The page does not inspect code in your editor. Share your local attempt path when requesting a code review.

See the [Spanish usage guide](docs/usage.md) for the complete workflow and recovery options.

## Layout

- `curriculum/`: dated agenda, exercise briefs, and sources.
- `exercises/`: runnable training projects and task definitions.
- `external/`: pinned upstream Gilded Rose practice, provenance, and license.
- `cases/`: original business-rule practice material.
- `behavioral/`: question banks and blank story templates.
- `attempts/`: private local attempts, ignored by Git.
- `private/`: private notes and exported progress, ignored by Git.
- `web/`: daily preparation interface.

## Development and checks

```bash
npm ci
./scripts/local.sh
# Local page: http://127.0.0.1:5187/grind/capital-one/
npm test
npm run build
uv run pytest
```

`uv run python scripts/practice.py verify` independently checks all original starter/reference pairs. Expected failures in starter code are intentional. The `check` command verifies the behavior covered by its tests, not interview readiness.

Deployment uses `scripts/deploy.sh` and the existing VPS static-hosting setup. Only `dist/` is uploaded; private notes and attempts remain local.

This is independent preparation material, not an official Capital One product or a guaranteed interview question bank. All exercise data is fictional. Personal answers and attempts are never published by the project.
