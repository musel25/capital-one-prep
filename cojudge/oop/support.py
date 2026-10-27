"""Build and verify the Python OOP course in the native CoJudge format.

Each ``specs/oNN.py`` exports ``SPEC``. The learner edits classes; a supplied
driver turns each test's steps into calls on them. Answers come from two
independent implementations: the Python reference and the Java Marker model.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

from cojudge.authoring.support import (
    ADAPTER, ROOT, check_java, encode, java_source, json_equal, python_solver, write_json,
)
from cojudge.oop.driver import DRIVER, JAVA_KIT

COURSE_ID = "python-oop"
PREFIX = "oop"
LEVELS = ["01-classes-and-properties", "02-state-and-behavior", "03-inheritance-and-composition",
          "04-dunder-methods-and-builtins", "05-small-projects"]
LEVEL_NAMES = ["Classes and properties", "State and behavior", "Inheritance and composition",
               "Dunder methods and built-ins", "Small projects"]
GENERATED = 20
SPEC_DIR = ROOT / "cojudge/oop/specs"


def problem_id(spec):
    return f"{PREFIX}-{spec['number']:02d}-{spec['slug']}"


def load_specs(numbers=None):
    specs = []
    for path in sorted(SPEC_DIR.glob("o[0-9][0-9].py")):
        if numbers and int(path.stem[1:]) not in numbers:
            continue
        module_spec = importlib.util.spec_from_file_location(f"oop_{path.stem}", path)
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = module
        module_spec.loader.exec_module(module)
        spec = module.SPEC
        if spec["number"] != int(path.stem[1:]):
            raise ValueError(f"Number does not match filename: {path}")
        specs.append(spec)
    return specs


def validate(spec):
    required = {"number", "slug", "title", "difficulty", "time", "level", "prerequisites", "learn",
                "scenario", "task", "constraints", "hints", "starter", "reference", "java", "facts",
                "approach", "cases", "example_notes", "generate", "mutations", "sources"}
    missing = required - spec.keys()
    if missing:
        raise ValueError(f"{spec.get('number')}: missing fields {sorted(missing)}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", spec["slug"]):
        raise ValueError("Invalid slug")
    if spec["difficulty"] not in {"Easy", "Medium", "Hard"} or spec["level"] not in range(1, 6):
        raise ValueError("Invalid difficulty or level")
    if len(spec["cases"]) < 10 or len(spec["example_notes"]) != 3:
        raise ValueError("Need at least 10 explicit cases and 3 example notes")
    for case in spec["cases"]:
        if not case.get("label") or "expected" not in case or len(case["expected"]) != len(case["ops"]):
            raise ValueError(f"Case needs a label and one expected value per step: {case.get('label')}")
    for mutation in spec["mutations"]:
        if mutation["old"] not in spec["reference"]:
            raise ValueError(f"Mutation target not found: {mutation['name']}")


def generated_inputs(spec):
    rng = random.Random(1000 + spec["number"])
    inputs, seen = [], {encode({"ops": case["ops"]}) for case in spec["cases"]}
    for _ in range(GENERATED * 5):
        data = json.loads(encode({"ops": spec["generate"](rng)}))
        key = encode(data)
        if key not in seen:
            seen.add(key)
            inputs.append(data)
        if len(inputs) == GENERATED:
            break
    if len(inputs) < GENERATED:
        raise ValueError(f"{problem_id(spec)}: generator repeats itself")
    return inputs


def full_source(classes):
    return classes.rstrip() + "\n" + DRIVER


def all_cases(spec):
    solve = python_solver(full_source(spec["reference"]))
    # The judge sends payloads with sorted keys, so answers are computed from that form.
    cases = [{"input": json.loads(encode({"ops": c["ops"]})), "expected": c["expected"], "label": c["label"]}
             for c in spec["cases"]]
    for i, data in enumerate(generated_inputs(spec)):
        cases.append({"input": data, "expected": json.loads(encode(solve(copy.deepcopy(data)))),
                      "label": f"generated-{i + 1}"})
    return cases


def judge_spec(spec):
    """The dictionary shape that authoring.support expects for Marker checks."""
    facts = ", ".join(json.dumps(f) for f in spec["facts"])
    java = JAVA_KIT + f"String[] facts() {{ return new String[]{{{facts}}}; }}\n" + spec["java"]
    return {"number": spec["number"], "slug": spec["slug"], "prefix": PREFIX, "java": java}


def check_python(spec):
    validate(spec)
    solve = python_solver(full_source(spec["reference"]))
    for case in spec["cases"]:
        actual = solve(json.loads(encode({"ops": case["ops"]})))
        assert json_equal(actual, case["expected"]), (
            f"{problem_id(spec)} case '{case['label']}':\n  actual   {encode(actual)}\n  expected {encode(case['expected'])}")
    cases = all_cases(spec)
    mutations = []
    for mutation in spec["mutations"]:
        bad = python_solver(full_source(spec["reference"].replace(mutation["old"], mutation["new"], 1)))
        killed = [i for i, case in enumerate(cases)
                  if not json_equal(bad(copy.deepcopy(case["input"])), case["expected"])]
        assert killed, f"{problem_id(spec)} mutation survived: {mutation['name']}"
        mutations.append({"name": mutation["name"], "detected_by": len(killed)})
    starter = python_solver(full_source(spec["starter"]))
    wrong = sum(not json_equal(starter(copy.deepcopy(c["input"])), c["expected"]) for c in cases)
    assert wrong >= 0.9 * len(cases), f"{problem_id(spec)}: the starter passes {len(cases) - wrong} cases"
    return {"id": problem_id(spec), "cases": len(cases), "explicit": len(spec["cases"]), "mutations": mutations}


def verify(spec, work):
    result = check_python(spec)
    result["java"] = check_java({**judge_spec(spec), "reference": full_source(spec["reference"]),
                                 "cases": all_cases(spec), "generated": []}, work)
    return result


DRIVER_NOTE = """Each test is a list of steps. The supplied driver at the bottom of the editor runs
the steps on your classes, in order, and records one result per step:

- A step that raises records `{"error": "ExceptionName"}`, and the test continues.
- An object of a class records `{"object": "ClassName"}`. Tuples show as lists.

| Step `do` | What the driver runs |
| --- | --- |
| `new` | `cls(*args, **kwargs)` |
| `get` / `set` | `obj.attr` / `obj.attr = value` (records `null`) |
| `call` | `obj.method(*args, **kwargs)`; `obj` can also be a class name |
| `invoke` | `obj(*args)` |
| `op` | `left <op> right`, for example `a + b` or `a @ b` |
| `item` / `setitem` | `obj[key]` / `obj[key] = value` |
| `repr`, `str`, `len`, `bool`, `list`, `sorted` | the built-in function on `obj` |
| `with` | `with obj as name:` runs the inner `body` steps; `raise` raises that exception at the end of the block. Records `{"body": [...], "error": null or "ExceptionName"}` |
| `check` | the class structure, for example `"is": "property"` checks that `cls.attr` is a `property` |

`"save": "x"` stores a step's result under the name `x`. `{"ref": "x"}` inside a value means
that stored object. Copy an example's input into a custom test to debug it."""


def statement(spec, cases):
    title = f"{spec['number']:02d}. {spec['title']}"
    references = ", ".join(f"[{i + 1}]({url})" for i, url in enumerate(spec["sources"]))
    return f"""# {title}

[Course list](/?course={COURSE_ID}) · Level {spec['level']}: {LEVEL_NAMES[spec['level'] - 1]} · {spec['difficulty']} · About {spec['time']} minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** {spec['prerequisites']}

{spec['learn'].strip()}

</details>

**Scenario:** {spec['scenario'].strip()}

{spec['task'].strip()}

**Constraints:**

""" + "\n".join(f"- {item}" for item in spec["constraints"]) + f"""

<details>
<summary><strong>How the tests work</strong></summary>

{DRIVER_NOTE}

</details>

---

Select **Python**. Write your classes above the driver line. Do not edit the driver or the
`Solution.run` adapter. **Run** checks the three examples. **Submit** runs all {len(cases)} tests.
This is an original practice exercise.

Python documentation: {references}
"""


def build_problem(spec, destination):
    check_python(spec)
    pid = problem_id(spec)
    folder = Path(destination) / "problems" / pid
    folder.mkdir(parents=True, exist_ok=True)
    instructor = Path(destination) / "instructor" / pid
    instructor.mkdir(parents=True, exist_ok=True)
    cases = all_cases(spec)
    category = LEVELS[spec["level"] - 1]
    metadata = {
        "id": pid, "title": f"{spec['number']:02d}. {spec['title']}", "difficulty": spec["difficulty"],
        "link": "", "category": category,
        "examples": [{"input": json.dumps(c["input"], ensure_ascii=True),
                      "output": json.dumps(c["expected"], ensure_ascii=True), "explanation": note}
                     for c, note in zip(cases[:3], spec["example_notes"])],
        "starterCode": {"python": full_source(spec["starter"]).rstrip() + ADAPTER},
        "testCases": [{"payload": encode(c["input"])} for c in cases[:3]],
        "functionName": "run", "params": [{"name": "payload", "type": "string"}],
        "outputType": "string", "hints": spec["hints"],
    }
    reference = full_source(spec["reference"]).rstrip() + ADAPTER
    write_json(folder / "metadata.json", metadata)
    write_json(folder / "official-tests.json", [{"payload": encode(c["input"])} for c in cases])
    (folder / "statement.md").write_text(statement(spec, cases))
    (folder / "Marker.java").write_text(java_source(judge_spec(spec)))
    (folder / "solution.md").write_text(
        f"## Approach\n\n{spec['approach'].strip()}\n\n## Reference classes\n\n"
        f"```python\n{spec['reference'].strip()}\n```\n")
    (instructor / "reference.py").write_text(reference)
    write_json(instructor / "cases.json", cases)
    return {"id": pid, "number": spec["number"], "title": spec["title"], "cases": len(cases), "category": category}


def course_info(records):
    return {
        "title": "Python OOP Path",
        "description": "22 original Python exercises on object-oriented programming. Start at 01. "
                       "Five levels: classes and properties, state and behavior, inheritance and "
                       "composition, dunder methods and built-ins, then three small projects. Select "
                       "Python. You write classes; a supplied driver calls them and checks the results "
                       "and some class structure. Open the collapsed lesson first if the topic is new.",
        "category-order": LEVELS,
        "problems-of-category": {level: [r["id"] for r in records if r["category"] == level]
                                 for level in LEVELS},
    }
