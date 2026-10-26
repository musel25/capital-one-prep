"""Export learner-facing lab briefs without instructor material."""
from pathlib import Path

from codebase_labs.runner import ROOT, load_labs


def build_briefs(destination=ROOT / "codebase_labs/briefs"):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for lab in load_labs():
        body = (f"# {lab['id']}: {lab['title']}\n\n"
                "[Back to the ordered course guide](../README.md)\n\n"
                f"**Objective:** {lab['objective']}\n\n"
                f"**Practice estimate:** {lab['minutes']} minutes.\n\n"
                f"Start a fresh attempt from the repository root:\n\n```sh\n"
                f"uv run python scripts/codebase.py start {lab['id']}\n```\n\n"
                "Open the printed folder and follow its README. It includes the exact check command.\n\n"
                + lab["brief"].strip() + "\n\n## Check the AI claim\n\n"
                "This is a constructed example. Assess it with code and tests.\n\n> "
                + lab["ai_claim"].replace("\n", "\n> ") + "\n\n## Official references\n\n"
                + "\n".join(f"- [Documentation {i+1}]({url})" for i, url in enumerate(lab["sources"])) + "\n")
        (destination / f"{lab['id']}.md").write_text(body)
