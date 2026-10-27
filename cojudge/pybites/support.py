"""Build and verify the Pybites OOP path as native CoJudge problems.

Each ``bites/bNN.py`` exports ``SPEC``: the bite's module name, template, pytest
tests, and a reference solution. The description comes from the public bite page
(``source-pages.json``). Verification runs the real runner with Python 3.11,
the judge's version: the reference must pass every test and the template must
fail at least one.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.pybites.runner import MARKER, RUNNER

COURSE_ID = "pybites-oop"
PREFIX = "pb"
LEVELS = ["01-beginner", "02-intermediate", "03-advanced"]
DIFFICULTY = {"Beginner": "Easy", "Intermediate": "Medium", "Advanced": "Hard"}
HERE = ROOT / "cojudge/pybites"
PYTHON = subprocess.run(["uv", "python", "find", "3.11"], capture_output=True, text=True).stdout.strip() or "python3"


def load_specs(numbers=None):
    pages = {page["n"]: page for page in json.loads((HERE / "source-pages.json").read_text())}
    specs = []
    for path in sorted((HERE / "bites").glob("b[0-9][0-9].py")):
        number = int(path.stem[1:])
        if numbers and number not in numbers:
            continue
        module_spec = importlib.util.spec_from_file_location(f"pybites_{path.stem}", path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        spec = {**module.SPEC, "number": number, "page": pages[number]}
        for field in ("template", "tests", "reference"):
            spec[field] = spec[field].replace("\r\n", "\n")
        specs.append(spec)
    return specs


def problem_id(spec):
    return f"{PREFIX}-{spec['number']:02d}-{re.sub(r'[^a-z0-9]+', '-', spec['page']['slug']).strip('-')}"


def tests_block(spec):
    tests = spec["tests"].strip("\n") + "\n"
    quote = "'''" if "'''" not in tests else '"""'
    block = f"r{quote}\n{tests}{quote}"
    assert eval(block)[1:] == tests, "tests cannot be embedded as a raw string"
    return ("\n\n# " + "-" * 75 + "\n"
            f"# Pybites tests. They import your code as the module `{spec['module']}`.\n"
            "# Read them to see what is expected. Do not edit them.\n"
            "# " + "-" * 75 + "\n"
            f"_PB_MODULE = {spec['module']!r}\n"
            f"_PB_TESTS = {block}[1:]\n")


def full_source(spec, code):
    return code.rstrip() + "\n" + tests_block(spec) + RUNNER


def run_all(spec, code):
    """Run every test through the real runner in Python 3.11; return {test id: result}."""
    with tempfile.TemporaryDirectory(prefix="pybites-") as work:
        (Path(work) / "Solution.py").write_text(full_source(spec, code))
        script = ("import json, sys\nfrom Solution import Solution\n"
                  "run = Solution().run\nids = json.loads(run(json.dumps({'test': '--list'})))\n"
                  "print(json.dumps({i: run(json.dumps({'test': i})) for i in ids}))\n")
        done = subprocess.run([PYTHON, "-c", script], cwd=work, capture_output=True, text=True, timeout=300)
        if done.returncode:
            raise AssertionError(f"{problem_id(spec)}: runner crashed\n{done.stderr[-2000:]}")
        return json.loads(done.stdout.strip().splitlines()[-1])


def verify(spec):
    results = run_all(spec, spec["reference"])
    failed = {k: v for k, v in results.items() if v != "passed"}
    assert results and not failed, f"{problem_id(spec)} reference fails: {failed}"
    starter = run_all(spec, spec["template"])
    assert any(v != "passed" for v in starter.values()), f"{problem_id(spec)}: the template passes every test"
    return {"id": problem_id(spec), "tests": list(results), "template_failures": sum(v != "passed" for v in starter.values())}


class _Markdown(HTMLParser):
    """Enough HTML-to-Markdown for the bite descriptions."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.href, self.pre, self.lists, self.cell = [], None, False, [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "pre":
            self.pre = True
            self.out.append("\n\n```python\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag == "em":
            self.out.append("*")
        elif tag == "a":
            self.href = attrs.get("href") or ""
            self.out.append("[" if self.href.startswith("http") else "")
        elif tag in ("ul", "ol"):
            self.lists.append(tag)
        elif tag == "li":
            self.out.append("\n" + "  " * (len(self.lists) - 1) + ("1. " if self.lists[-1:] == ["ol"] else "- "))
        elif tag in ("h2", "h3", "h4"):
            self.out.append("\n\n### ")
        elif tag == "br":
            self.out.append("\n")
        elif tag == "hr":
            self.out.append("\n\n---\n\n")
        elif tag == "blockquote":
            self.out.append("\n\n> ")
        elif tag == "tr":
            self.out.append("\n")
        elif tag == "td":
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.pre = False
            self.out.append("\n```\n\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag == "em":
            self.out.append("*")
        elif tag == "a":
            self.out.append(f"]({self.href})" if self.href.startswith("http") else "")
        elif tag in ("ul", "ol"):
            self.lists.pop()
            self.out.append("\n\n")
        elif tag in ("p", "h2", "h3", "h4", "div", "table"):
            self.out.append("\n\n")

    def handle_data(self, data):
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))


def description(spec):
    parser = _Markdown()
    parser.feed(spec["page"]["desc_html"])
    text = "".join(parser.out)
    text = re.sub(r"```python\n\s*>>>", "```python\n>>>", text)
    # Outside code blocks, drop indentation and trailing spaces left by the HTML.
    parts = text.split("```")
    for i in range(0, len(parts), 2):
        parts[i] = "\n".join(line.strip() if not line.lstrip().startswith(("- ", "1. ")) else line.rstrip()
                             for line in parts[i].split("\n"))
    text = "```".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return html.unescape(text).strip()


def statement(spec, test_ids):
    page = spec["page"]
    url = f"https://pybitesplatform.com/bites/{page['slug']}/"
    origin = ("The template and tests are the originals from this free bite."
              if spec.get("original") else
              "The original template and tests are in Pybites premium, so the template and tests here "
              "are a recreation that follows the description.")
    notes = f"\n\n**Notes for this version:** {spec['notes'].strip()}" if spec.get("notes") else ""
    return f"""# {spec['number']:02d}. {spec['title']}

[Course list](/?course={COURSE_ID}) · Pybites {page['level']} · [Original bite]({url})

{description(spec)}{notes}

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `{spec['module']}`. **Run** checks the first three tests. **Submit** runs all
{len(test_ids)}. A failing test shows its name, the error, and the failed test line. {origin}

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
"""


def build_problem(spec, destination):
    result = verify(spec)
    pid, ids = result["id"], result["tests"]
    folder = Path(destination) / "problems" / pid
    folder.mkdir(parents=True, exist_ok=True)
    payloads = [json.dumps({"test": test_id}) for test_id in ids]
    metadata = {
        "id": pid, "title": f"{spec['number']:02d}. {spec['title']}",
        "difficulty": DIFFICULTY[spec["page"]["level"]], "link": "",
        "category": LEVELS[list(DIFFICULTY).index(spec["page"]["level"])],
        "examples": [{"input": p, "output": "passed", "explanation": f"Test {i} must pass."}
                     for p, i in zip(payloads[:3], ids[:3])],
        "starterCode": {"python": full_source(spec, spec["template"])},
        "testCases": [{"payload": p} for p in payloads[:3]],
        "functionName": "run", "params": [{"name": "payload", "type": "string"}],
        "outputType": "string", "hints": spec.get("hints", []),
    }
    write_json(folder / "metadata.json", metadata)
    write_json(folder / "official-tests.json", [{"payload": p} for p in payloads])
    (folder / "statement.md").write_text(statement(spec, ids))
    (folder / "Marker.java").write_text(MARKER)
    (folder / "solution.md").write_text(
        f"## Reference solution\n\n```python\n{spec['reference'].strip()}\n```\n")
    return {**result, "number": spec["number"], "category": metadata["category"], "cases": len(ids)}


def course_info(records):
    return {
        "title": "Pybites OOP Path",
        "description": "The 22 bites of the Pybites Object Oriented Programming learning path, in the same "
                       "order. Each problem has the bite's description, a code template, and its pytest "
                       "tests, which the judge runs on your code. Bites 1 and 14 use the original free "
                       "template and tests; the others are recreations that follow the public descriptions. "
                       "Select Python.",
        "category-order": LEVELS,
        "problems-of-category": {level: [r["id"] for r in records if r["category"] == level] for level in LEVELS},
    }
