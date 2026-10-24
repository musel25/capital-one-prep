# Capital One Prep

A ten-day preparation workspace for Capital One TDP Mexico, October 23–November 1, 2026. Three hours and forty-five minutes each day: AI-assisted debugging and feature work, technical business cases, behavioral practice, and targeted Python exercises.

The daily page provides the agenda. Code is practiced in your own editor, with independent attempt folders that preserve your work. Instructions are in Spanish; interview practice is in English.

**Open the planner:** [timer.musel.dev/grind/capital-one/](https://timer.musel.dev/grind/capital-one/)

**First visit?** Open [Empieza aquí: the website walkthrough](https://timer.musel.dev/grind/capital-one/?view=guide) for the daily workflow, a complete first-exercise example, timer controls, and progress backups.

## Start practicing

```bash
cd /home/musel/Github/capital-one-prep
uv sync
uv run python scripts/practice.py start d01-bug
```

Open the newly printed directory in your editor and read its README. It includes the startup commands and the exact task. Run `start` again for a fresh attempt; it never overwrites previous work. To check a solution, run `uv run python scripts/practice.py check attempts/YOUR-ATTEMPT` from the repository root.

The schedule has 40 blocks across ten days, including 20 independent debugging/feature tasks, ten technical cases, behavioral questions with follow-ups, and Python practice. Four LeetCode alternatives fit inside the existing time allocation. The site includes phase timers, checklists, notes, and gated case explanations. Behavioral blocks include project-based worksheets. Python blocks include copyable prompts for creating local starters and tests without solutions. There is no separate closing block.

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
