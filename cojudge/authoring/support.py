"""Build native CoJudge content and verify two independent implementations."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = '''

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
'''
LEVELS = [
    "01-python-data-and-libraries", "02-objects-and-state",
    "03-apis-and-clients", "04-sql-and-transactions", "05-system-components",
]


def encode(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":"))


def json_equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(json_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    return a == b


def slug(spec):
    return f"{spec.get('prefix', 'c1')}-{spec['number']:02d}-{spec['slug']}"


def load_specs(numbers=None):
    specs = []
    for path in sorted((ROOT / "cojudge/authoring").glob("p[0-9][0-9].py")):
        if numbers and int(path.stem[1:]) not in numbers:
            continue
        module_spec = importlib.util.spec_from_file_location(f"author_{path.stem}", path)
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = module
        module_spec.loader.exec_module(module)
        if module.SPEC["number"] != int(path.stem[1:]):
            raise ValueError(f"Number does not match filename: {path}")
        specs.append(module.SPEC)
    return specs


def validate_spec(spec):
    required = {"number", "slug", "title", "difficulty", "time", "prerequisites",
                "learn", "task", "constraints", "hints", "starter", "reference",
                "java", "approach", "cases", "generated", "mutations", "sources"}
    missing = required - spec.keys()
    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")
    if not 1 <= spec["number"] <= 50 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", spec["slug"]):
        raise ValueError("Invalid problem number or slug")
    for name in ("prefix", "course_id", "category"):
        if name in spec and (not isinstance(spec[name], str) or not re.fullmatch(
                r"[a-z0-9]+(?:-[a-z0-9]+)*", spec[name])):
            raise ValueError(f"Invalid course metadata: {name}")
    if "level" in spec and (type(spec["level"]) is not int or spec["level"] < 1):
        raise ValueError("Invalid course metadata: level")
    if spec["difficulty"] not in {"Easy", "Medium", "Hard"}:
        raise ValueError("Invalid difficulty")
    if len(spec["cases"]) < 12 or len(spec["generated"]) < 12:
        raise ValueError("Need at least 12 explicit and 12 additional cases")
    seen = set()
    for data in [case["input"] for case in spec["cases"]] + spec["generated"]:
        if not isinstance(data, dict):
            raise ValueError("Every input must be an object")
        key = encode(data)
        if key in seen:
            raise ValueError(f"duplicate input: {key[:140]}")
        seen.add(key)
    for case in spec["cases"]:
        encode(case["expected"])
        if not case.get("label"):
            raise ValueError("Explicit cases need labels")
    if "example_notes" in spec and len(spec["example_notes"]) != 3:
        raise ValueError("example_notes must explain the first three cases")
    if not spec["mutations"]:
        raise ValueError("Need at least one realistic mutation")
    for mutation in spec["mutations"]:
        if not mutation["old"] or mutation["old"] not in spec["reference"]:
            raise ValueError(f"Mutation target not found: {mutation['name']}")


def python_solver(source):
    # dataclasses resolves its defining module through sys.modules.
    name = "course_solution_" + hashlib.sha256(source.encode()).hexdigest()[:16]
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(compile(source, name, "exec"), module.__dict__)
    return module.solve


def all_cases(spec):
    solve = python_solver(spec["reference"])
    cases = copy.deepcopy(spec["cases"])
    for i, data in enumerate(spec["generated"]):
        result = solve(copy.deepcopy(data))
        cases.append({"input": copy.deepcopy(data), "expected": json.loads(encode(result)),
                      "label": f"additional-{i + 1}"})
    return cases


def check_python(spec):
    validate_spec(spec)
    solve = python_solver(spec["reference"])
    for i, case in enumerate(spec["cases"]):
        actual = solve(copy.deepcopy(case["input"]))
        assert json_equal(actual, case["expected"]), (
            f"{slug(spec)} case {i} ({case['label']}): {actual!r} != {case['expected']!r}"
        )
    cases = all_cases(spec)
    # Repeat inputs in reverse order to detect accidental module-state leakage.
    for case in reversed(cases):
        assert json_equal(solve(copy.deepcopy(case["input"])), case["expected"]), (
            f"{slug(spec)} state leakage: {case['label']}"
        )
    mutations = []
    for mutation in spec["mutations"]:
        source = spec["reference"].replace(mutation["old"], mutation["new"], mutation.get("count", 1))
        bad_solve = python_solver(source)  # Syntax errors do not count as a killed bug.
        killed = []
        for i, case in enumerate(cases):
            try:
                wrong = bad_solve(copy.deepcopy(case["input"]))
                if not json_equal(wrong, case["expected"]):
                    killed.append(i)
            except Exception:
                killed.append(i)
        assert killed, f"{slug(spec)} mutation survived: {mutation['name']}"
        mutations.append({"name": mutation["name"], "detected_by": killed})
    return {"id": slug(spec), "cases": len(cases), "explicit": len(spec["cases"]), "mutations": mutations}


def java_source(spec):
    support = (ROOT / "cojudge/authoring/Support.java").read_text()
    # Imports must precede all class definitions in the standalone marker file.
    support = support.replace("import java.util.*;\n", "").replace("import java.math.*;\n", "")
    return '''import java.util.*;
import java.math.*;
import java.time.*;
import java.time.format.*;
import java.util.regex.*;
import java.nio.charset.StandardCharsets;

class Marker extends Support {
''' + spec["java"] + '''
    public String run(String payload) { return J.dump(solve(obj(J.parse(payload)))); }
    public boolean isCorrect(String payload, String output) {
        try { return J.equal(J.parse(run(payload)), J.parse(output)); }
        catch (Exception error) { return false; }
    }
}
''' + support


JAVA_CHECK = '''import java.util.*;
import java.io.*;
class Verify extends Support {
    public static void main(String[] args) throws Exception {
        BufferedReader input = new BufferedReader(new InputStreamReader(System.in, java.nio.charset.StandardCharsets.UTF_8));
        Marker marker = new Marker();
        String line;
        int count = 0, rejected = 0;
        while ((line = input.readLine()) != null) {
            Map<String,Object> test = obj(J.parse(line));
            String payload = J.dump(test.get("input"));
            Object expected = test.get("expected");
            String actual = marker.run(payload);
            if (!J.equal(J.parse(actual), expected))
                throw new AssertionError("Case " + count + " " + test.get("label") + ": " + actual + " != " + J.dump(expected));
            if (!marker.isCorrect(payload, " \\n" + J.dump(expected) + "\\t "))
                throw new AssertionError("Rejected correct formatted JSON at " + count);
            for (Object wrong : list(null, true, false, 0, "incorrect", list(), map("__wrong__", true))) {
                if (!J.equal(expected, wrong)) {
                    if (marker.isCorrect(payload, J.dump(wrong)))
                        throw new AssertionError("Accepted wrong output at " + count + ": " + J.dump(wrong));
                    rejected++;
                }
            }
            for (String invalid : new String[]{"", "NaN", "{", "true false", "01", "{\\\"x\\\":1,\\\"x\\\":2}"}) {
                if (marker.isCorrect(payload, invalid)) throw new AssertionError("Accepted invalid JSON");
                rejected++;
            }
            for (String token : new String[]{"u+041", "u-001"}) {
                String invalid = Character.toString(34) + Character.toString(92) + token + Character.toString(34);
                if (marker.isCorrect(payload, invalid)) throw new AssertionError("Accepted invalid Unicode escape");
                rejected++;
            }
            count++;
        }
        System.out.println(J.dump(map("cases", count, "wrong_rejected", rejected)));
    }
}
'''


def check_java(spec, work_root):
    work = Path(work_root) / slug(spec)
    work.mkdir(parents=True, exist_ok=True)
    (work / "Marker.java").write_text(java_source(spec))
    (work / "Verify.java").write_text(JAVA_CHECK)
    compiled = subprocess.run(["javac", "-encoding", "UTF-8", "Marker.java", "Verify.java"],
                              cwd=work, capture_output=True, text=True, timeout=45)
    assert compiled.returncode == 0, f"{slug(spec)} compile: {compiled.stderr}"
    data = "\n".join(encode(case) for case in all_cases(spec)) + "\n"
    checked = subprocess.run(["java", "-Xmx256m", "Verify"], cwd=work, input=data,
                             capture_output=True, text=True, timeout=45)
    assert checked.returncode == 0, f"{slug(spec)} Java check: {checked.stdout}\n{checked.stderr}"
    return json.loads(checked.stdout)


def check_review_cases(spec, work_root, run_java=True):
    """Keep independently authored expectations separate from generated cases."""
    path = ROOT / "cojudge/authoring/review-cases.json"
    cases = json.loads(path.read_text())[str(spec.get("source_number", spec["number"]))]
    solve = python_solver(spec["reference"])
    official_inputs = {encode(c["input"]) for c in all_cases(spec)}
    for case in cases:
        assert encode(case["input"]) not in official_inputs, "Review case duplicates an official input"
        assert json_equal(solve(copy.deepcopy(case["input"])), case["expected"]), (
            f"{slug(spec)} reviewer case failed: {case['label']}"
        )
    report = {"cases": len(cases)}
    if run_java:
        report["java"] = check_java({**spec, "cases": cases, "generated": []}, work_root)
    return report


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True, allow_nan=False) + "\n")


def build_problem(spec, destination):
    check_python(spec)
    destination = Path(destination)
    problem_id = slug(spec)
    folder = destination / "problems" / problem_id
    folder.mkdir(parents=True, exist_ok=True)
    instructor = destination / "instructor" / problem_id
    instructor.mkdir(parents=True, exist_ok=True)
    cases = all_cases(spec)
    examples = [
        {"input": json.dumps(c["input"], ensure_ascii=True),
         "output": json.dumps(c["expected"], ensure_ascii=True), "explanation": note}
        for c, note in zip(cases[:3], spec.get("example_notes", [c["label"] for c in cases[:3]]))
    ]
    metadata = {
        "id": problem_id, "title": f"{spec['number']:02d}. {spec['title']}",
        "difficulty": spec["difficulty"],
        # CoJudge labels this optional link as LeetCode. These are original tasks.
        "link": "",
        "category": spec.get("category", LEVELS[(spec["number"] - 1) // 10]),
        "examples": examples, "starterCode": {"python": spec["starter"].rstrip() + ADAPTER},
        "testCases": [{"payload": encode(c["input"])} for c in cases[:3]],
        "functionName": "run", "params": [{"name": "payload", "type": "string"}],
        "outputType": "string", "hints": spec["hints"],
    }
    # CoJudge renders metadata examples between the text before "**Constraints:**" and the rest.
    scenario = f"**Scenario:** {spec['scenario'].strip()}\n\n" if spec.get("scenario") else ""
    ticket = f"> **Bug report:** {spec['ticket'].strip()}\n\n" if spec.get("ticket") else ""
    fix = f"\n\n**What to fix:** {spec['fix'].strip()}" if spec.get("fix") else ""
    practice = (f"\n\n<details>\n<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>\n\n"
                f"{spec['practice'].strip()}\n\n</details>") if spec.get("practice") else ""
    references = ", ".join(f"[{i + 1}]({url})" for i, url in enumerate(spec["sources"]))
    statement = f"""# {metadata['title']}

[Course list](/?course={spec.get('course_id', 'capital-one-engineering-50')}) · Level {spec.get('level', (spec['number'] - 1) // 10 + 1)} · {spec['difficulty']} · About {spec['time']} minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** {spec['prerequisites']}

{spec['learn'].strip()}

</details>

{scenario}{ticket}{spec['task'].strip()}{fix}

**Constraints:**

""" + "\n".join(f"- {item}" for item in spec["constraints"]) + practice + f"""

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all {len(cases)} tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.
""" + (f"\n{spec['next'].strip()}\n" if spec.get("next") else "") + f"\nOfficial documentation: {references}\n"
    reference = spec["reference"].rstrip() + ADAPTER
    write_json(folder / "metadata.json", metadata)
    write_json(folder / "official-tests.json", [{"payload": encode(c["input"])} for c in cases])
    (folder / "statement.md").write_text(statement)
    (folder / "Marker.java").write_text(java_source(spec))
    (folder / "solution.md").write_text(
        f"## Approach\n\n{spec['approach'].strip()}\n\n## Python implementation\n\n```python\n{reference}\n```\n"
    )
    (instructor / "reference.py").write_text(reference)
    write_json(instructor / "cases.json", cases)
    write_json(instructor / "mutation-report.json", check_python(spec)["mutations"])
    return {"id": problem_id, "number": spec["number"], "title": spec["title"],
            "cases": len(cases), "category": metadata["category"]}
