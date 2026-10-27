"""Build guided repairs from independently verified behavioral contracts."""
import copy
import json
import re

from cojudge.authoring.support import ROOT, load_specs, slug

COURSE_ID = "capital-one-codebase-practice"
GUIDE_URL = "https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md"
LEVELS = ["01-read-data-and-state", "02-follow-objects-and-control-flow",
          "03-trace-api-contracts", "04-test-client-boundaries"]
SOURCE_NUMBERS = [3, 7, 11, 12, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 30]
PREREQUISITES = [
    "Lists, dictionaries, loops, and functions. This is the first exercise in this course.",
    "Exercise 01. Read dictionary keys, return values, and rejection paths.",
    "Exercises 01–02. The lesson introduces dataclasses and per-instance state.",
    "Exercise 03. Follow references to dictionaries and nested lists.",
    "Exercises 01–04 and local labs 01–02. The lesson introduces inherited method calls.",
    "Exercise 05. Follow an object method call and read an integer calculation.",
    "Exercises 05–06. Read a sequence of operations that updates object state.",
    "Exercise 07. Trace accepted and rejected state transitions.",
    "Exercises 01–08 and local labs 01–04. The lesson introduces HTTP route decisions.",
    "Exercise 09. Read request bodies and the runtime validation checks from exercise 02.",
    "Exercises 09–10. Distinguish an absent field from an explicit null value.",
    "Exercise 11. Trace a request through validation, lookup, and a state update.",
    "Exercises 09–12 and local labs 05–06. Read tuple ordering and page cursors.",
    "Exercise 13. Follow an ordered list of outcomes and a retry counter.",
    "Exercise 14. Read retry decisions and integer time values.",
    "Exercises 13–15. Trace cursor, duplicate, timeout, and error state through one loop.",
]


def load_codebase_specs(numbers=None):
    from cojudge.codebase.lessons import LESSONS

    assert [lesson["number"] for lesson in LESSONS] == list(range(1, 17))
    assert [lesson["source_number"] for lesson in LESSONS] == SOURCE_NUMBERS
    originals = {spec["number"]: spec for spec in load_specs(SOURCE_NUMBERS)}
    specs = []
    for lesson in LESSONS:
        if numbers and lesson["number"] not in numbers:
            continue
        source = originals[lesson["source_number"]]
        spec = copy.deepcopy(source)
        number = lesson["number"]
        level = (number - 1) // 4 + 1
        mutation = source["mutations"][0]
        starter = source["reference"].replace(mutation["old"], mutation["new"], mutation.get("count", 1))
        spec.update(number=number, source_number=source["number"], prefix="cb", course_id=COURSE_ID,
                    level=level, category=LEVELS[level - 1], title=lesson["title"], time=source["time"] + 10,
                    prerequisites=PREREQUISITES[number - 1],
                    starter="# This existing program has one intentional behavior defect.\n"
                            "# Read the task. Write a regression case before changing it.\n" + starter)
        spec["ticket"] = lesson["ticket"]
        spec["learn"] = lesson["orientation"] + "\n\n" + source["learn"]
        # A bug-fix source opens with its own defect note; show it once, under "What to fix".
        lead = "The starter runs, but it has one intentional bug."
        if source["task"].startswith("**Bug fix.** "):
            note, spec["task"] = source["task"].split("\n\n", 1)
            lead += " " + note.removeprefix("**Bug fix.** ")
        spec["fix"] = (lead + "\n\n"
                       + "\n".join("- " + rule for rule in re.split(r"(?<=\.)\s+(?=[A-Z])", lesson["scope"])))
        spec["practice"] = ("### Worked trace\n\n" + lesson["trace"]
                            + "\n\n### Read the existing code\n\n" + lesson["read"]
                            + "\n\n### Test before and after the change\n\n" + lesson["test_plan"]
                            + "\n\n### Check an AI claim\n\nThe following claim is a constructed review example. "
                            "It may be correct or incorrect. Check it against the code and contract.\n\n> "
                            + lesson["ai_claim"].replace("\n", "\n> ")
                            + "\n\nOptional AI prompt. Write your own implementation and tests:\n\n> "
                            + lesson["ai_prompt"].replace("\n", "\n> ")
                            + "\n\n### Technical completion checks\n\n"
                            + "\n".join("- " + item for item in lesson["done"])
                            + "\n\nA judge pass checks behavior. Your trace, test choice, and edit scope "
                            "need your review. Do not use the pass mark as evidence of those skills.")
        spec["next"] = f"[Full sequence and local pytest labs]({GUIDE_URL}). "
        if number % 4 == 0:
            first_lab = level * 2 - 1
            spec["next"] += f"Next, complete lab{first_lab:02d} and lab{first_lab+1:02d} from the guide."
        else:
            next_source = originals[SOURCE_NUMBERS[number]]
            next_id = slug({**next_source, "number": number + 1, "prefix": "cb"})
            spec["next"] += f"Then open [exercise {number+1:02d}](/problems/{next_id})."
        spec["approach"] += ("\n\n## Review of the AI claim\n\n" + lesson["ai_answer"]
                             + f"\n\n## Provenance\n\nThis guided repair reuses the verified behavior contract "
                             f"and independent oracle from Engineering 50 problem {source['number']:02d}. "
                             "The starter, reading task, test plan, and AI review exercise form a new lesson.")
        specs.append(spec)
    return specs


def review_cases(spec):
    original = json.loads((ROOT / "cojudge/authoring/review-cases.json").read_text())[str(spec["source_number"])]
    lessons = json.loads((ROOT / "cojudge/codebase/lesson-review-cases.json").read_text())[str(spec["number"])]
    return original + lessons


def course_info(records):
    return {
        "title": "Codebase Practice: Read, Test, Change",
        "description": "Start at 01. Read existing Python code, predict its behavior, write a regression case, "
                       "and make one scoped repair. Four levels cover data and state, objects and control flow, "
                       "API contracts, and client boundaries. After each four browser exercises, complete two "
                       "short local pytest labs. You write the code and tests. AI is optional for explanations "
                       "and reviews. The full 24-step guide is at " + GUIDE_URL + ". Select Python. "
                       "SQL is optional extended practice. This is constructed training, not an official "
                       "Capital One syllabus or a readiness score.",
        "category-order": LEVELS,
        "problems-of-category": {level: [r["id"] for r in records if r["category"] == level] for level in LEVELS},
    }
