"""Preserve learner work and grade behavior and test evidence in temporary copies."""
from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".venv", ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules"}


def load_labs():
    labs = []
    for path in sorted((ROOT / "codebase_labs").glob("lab[0-9][0-9].py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        lab = module.LAB
        if lab["id"] != path.stem or lab["kind"] not in {"tests", "repair", "feature"}:
            raise ValueError(f"Invalid authored lab: {path.name}")
        for name in lab["files"]:
            _relative(name)
        for files in [lab["reference"], *[v["files"] for v in lab["variants"]]]:
            for name in files:
                _relative(name)
                if not name.startswith("app/"):
                    raise ValueError("Instructor variants may replace application files only")
        labs.append(lab)
    return labs


def _relative(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"Unsafe authored path: {name!r}")
    return path


def _lab(lab_id):
    matches = [lab for lab in load_labs() if lab["id"] == lab_id]
    if len(matches) != 1:
        raise ValueError(f"Unknown lab: {lab_id!r}")
    return matches[0]


def _write_files(destination, files):
    for name, source in files.items():
        target = destination / _relative(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source)


def _readme(lab, destination):
    return f"""# {lab['id']}: {lab['title']}

**Objective:** {lab['objective']}

**Practice estimate:** {lab['minutes']} minutes. Continue when needed.

{lab['brief'].strip()}

## Check the AI claim

This is a constructed review example. Use code and tests to assess it.

> {lab['ai_claim']}

## Start and check this attempt

From this folder:

```sh
cd "{destination}"
uv sync
uv run pytest -q tests/test_existing.py
uv run pytest -q tests/learner
```

The learner test file starts empty. Pytest reports no tests until you write them.
Use `uv run pytest --collect-only -q tests/learner` to inspect collection.

After writing your tests and any assigned change:

```sh
uv run --project "{ROOT}" python "{ROOT / 'scripts/codebase.py'}" check "{destination}"
```

The checker runs a temporary copy. It checks your tests against correct code and
faulty variants. A crash or import error does not count as detecting a defect.
Repair and feature labs also check your implementation against separate contracts.
Exit 0 means sampled success, 1 means missing behavior or test evidence, and 2
means a setup or execution error. Read the reported phase before changing code.

Keep your work here. Starting again creates another folder. Use AI for a narrow
explanation or review after your own trace and test prediction. Write the code
and tests yourself. Record which AI claims your evidence supports or rejects.
No spoken explanation or behavioral-interview task is required.

This is constructed technical practice. It is not an official Capital One task.
Passing finite tests does not prove code quality or interview readiness. This is
a local checker for your own code, not a security sandbox for untrusted code.
"""


def _build(lab, destination):
    _write_files(destination, lab["files"])
    for name in ("pyproject.toml", "uv.lock"):
        shutil.copy2(ROOT / name, destination / name)
    (destination / ".codebase-lab.json").write_text(json.dumps(
        {"schema_version": 1, "lab_id": lab["id"]}, indent=2) + "\n")
    (destination / "README.md").write_text(_readme(lab, destination))


def start(lab_id, output_root=ROOT / "attempts"):
    lab = _lab(lab_id)
    output_root = Path(output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    destination = output_root / f"codebase-{lab_id}-{stamp}-{uuid.uuid4().hex[:8]}"
    destination.mkdir(exist_ok=False)
    _build(lab, destination)
    return destination


def _editable(name, lab):
    return any(name.startswith(rule) if rule.endswith("/") else name == rule for rule in lab["editable"])


def _validate_attempt(path):
    path = Path(path).expanduser()
    if path.is_symlink():
        raise ValueError("Attempt root is a symlink")
    path = path.resolve()
    marker = path / ".codebase-lab.json"
    if not marker.is_file() or marker.is_symlink():
        raise ValueError("Missing or unsafe lab manifest")
    try:
        data = json.loads(marker.read_text())
        if (not isinstance(data, dict) or type(data.get("schema_version")) is not int
                or data["schema_version"] != 1 or not isinstance(data.get("lab_id"), str)
                or not re.fullmatch(r"lab[0-9]{2}", data["lab_id"])):
            raise ValueError("Invalid lab manifest")
        lab = _lab(data["lab_id"])
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        raise ValueError(f"Invalid lab manifest: {error}") from error
    for directory, dirs, files in os.walk(path, followlinks=False):
        dirs[:] = [name for name in dirs if name not in IGNORED]
        for name in dirs + files:
            target = Path(directory) / name
            if target.is_symlink():
                raise ValueError(f"Unexpected symlink: {target.relative_to(path)}")
    for name, expected in lab["files"].items():
        if not _editable(name, lab):
            target = path / name
            if not target.is_file() or target.read_text() != expected:
                raise ValueError(f"Outside the lab edit scope: {name}")
    for parent in ("app", "tests"):
        for target in (path / parent).rglob("*.py"):
            name = target.relative_to(path).as_posix()
            if name not in lab["files"] and not _editable(name, lab):
                raise ValueError(f"Outside the lab edit scope: {name}")
    return path, lab


def _pytest(work, paths):
    report = work / (".pytest-evidence-" + uuid.uuid4().hex + ".xml")
    env = {**os.environ, "PYTHONPATH": str(work), "PYTHONDONTWRITEBYTECODE": "1",
           "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
    command = ["uv", "run", "--project", str(ROOT), "--no-sync", "python", "-m", "pytest",
               "-q", "--tb=line", "-c", str(work / "pyproject.toml"), "-o", "addopts=",
               "--junitxml", str(report), *paths]
    try:
        completed = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        return {"exit_code": 2, "errors": 1, "passed": 0, "assertions": 0,
                "other_failures": 0, "output": "Pytest exceeded the 90-second execution limit."}
    result = {"exit_code": completed.returncode, "errors": 0, "passed": 0, "assertions": 0,
              "other_failures": 0, "output": (completed.stdout + completed.stderr)[-5000:]}
    if not report.is_file():
        result["errors"] = 1
        return result
    try:
        cases = ET.parse(report).getroot().iter("testcase")
        for case in cases:
            failure = case.find("failure")
            if case.find("error") is not None:
                result["errors"] += 1
            elif failure is not None:
                message = failure.get("message", "")
                if message == "AssertionError" or message.startswith(("AssertionError:", "assert ", "Failed:")):
                    result["assertions"] += 1
                else:
                    result["other_failures"] += 1
            elif case.find("skipped") is None:
                result["passed"] += 1
    except ET.ParseError:
        result["errors"] += 1
    return result


def _failure(result, phase, rejected):
    is_error = result["errors"] or result["other_failures"] or result["exit_code"] not in (0, 1, 5)
    return {"status": "error" if is_error else "failed", "phase": phase,
            "mutations_rejected": list(rejected), "evidence": result}


def check(path):
    path, lab = _validate_attempt(path)
    rejected = []
    with tempfile.TemporaryDirectory(prefix="codebase-check-") as temporary:
        work = Path(temporary) / "attempt"
        shutil.copytree(path, work, ignore=shutil.ignore_patterns(*IGNORED))
        candidate = _pytest(work, ["tests"])
        if candidate["exit_code"] != 0:
            return _failure(candidate, "your-tests", rejected)
        if lab["kind"] != "tests":
            _write_files(work, {"_coach_checks/test_contract.py": lab["contract_tests"]})
            contract = _pytest(work, ["_coach_checks/test_contract.py"])
            if contract["exit_code"] != 0:
                return _failure(contract, "implementation-contract", rejected)
        correct_files = {name: source for name, source in lab["files"].items() if name.startswith("app/")}
        correct_files.update(lab["reference"])
        _write_files(work, correct_files)
        reference = _pytest(work, ["tests/learner"])
        if reference["exit_code"] != 0 or reference["passed"] == 0:
            return _failure(reference, "learner-reference", rejected)
        for variant in lab["variants"]:
            _write_files(work, {**correct_files, **variant["files"]})
            result = _pytest(work, ["tests/learner"])
            if (result["exit_code"] != 1 or result["errors"] or result["other_failures"]
                    or not result["assertions"]):
                return _failure(result, "mutation: " + variant["name"], rejected)
            rejected.append(variant["name"])
    return {"status": "passed", "phase": "complete", "lab_id": lab["id"],
            "reference_tests_passed": reference["passed"], "mutations_rejected": rejected}


def verify():
    results = []
    labs = load_labs()
    assert [lab["id"] for lab in labs] == [f"lab{number:02d}" for number in range(1, 9)]
    with tempfile.TemporaryDirectory(prefix="codebase-author-check-") as temporary:
        for lab in labs:
            path = start(lab["id"], Path(temporary))
            public = _pytest(path, ["tests/test_existing.py"])
            assert public["exit_code"] == 0 and public["passed"], (lab["id"], "starter public", public)
            _write_files(path, {"_coach_checks/test_contract.py": lab["contract_tests"]})
            starter = _pytest(path, ["_coach_checks/test_contract.py"])
            if lab["kind"] == "tests":
                assert starter["exit_code"] == 0, (lab["id"], "test-only starter contract", starter)
            else:
                assert (starter["exit_code"] == 1 and starter["assertions"]
                        and not starter["errors"] and not starter["other_failures"]), (
                            lab["id"], "starter must fail an assertion", starter)
            _write_files(path, lab["reference"])
            _write_files(path, {"tests/learner/test_task.py": lab["reference_tests"]})
            result = check(path)
            assert result["status"] == "passed", (lab["id"], result)
            result["starter_public_tests"] = public["passed"]
            result["starter_contract_assertions"] = starter["assertions"]
            results.append(result)
            print(f"PASS {lab['id']}: {result['reference_tests_passed']} learner tests; "
                  f"{len(result['mutations_rejected'])} faulty variants rejected", flush=True)
    return {"labs": results, "failures": []}
