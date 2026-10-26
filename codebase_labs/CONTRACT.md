# Local lab authoring contract

Each `labNN.py` exports `LAB`. Author only your assigned files. Do not change
attempts, private notes, the runner, or another author's labs. Do not commit;
the coordinator commits and immediately pushes coherent reviewed units.

```python
LAB = {
    "id": "lab01",
    "title": "Trace the intake pipeline",
    "kind": "tests",  # tests, repair, or feature
    "after": 4,  # browser exercise number; 01–02 after4, 03–04 after8, etc.
    "minutes": 35,
    "objective": "One specific technical skill.",
    "brief": "Self-contained Markdown contract and lesson; see required sections below.",
    "editable": ["tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/main.py": "... runnable starter source ...",
        "tests/test_existing.py": "... real supported-behavior tests ...",
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {"app/main.py": "... correct replacement source ..."},
    "contract_tests": "... pytest tests of the required implementation behavior ...",
    "reference_tests": "... sample learner pytest tests; never copied into attempts ...",
    "variants": [
        {"name": "accepts booleans", "files": {"app/main.py": "... faulty complete file ..."}},
    ],
    "ai_claim": "A plausible constructed AI claim the learner must check.",
    "ai_answer": "Instructor-only assessment with a concrete counterexample.",
    "sources": ["official documentation URLs"],
}
```

File paths must be relative, without `..` or symlinks. Use package `app` in each
snapshot. No file called `pyproject.toml`, lockfile, manifest, or generated README
in `files`; the runner supplies these. Python >=3.12 and current repository
dependencies are available. Use only Python standard library, pytest, FastAPI,
and httpx. Run with uv. No network, real sleep, randomness, or clock dependence.

`reference` replaces only files that differ from the starter. A correct snapshot
is `files` overlaid with `reference`. A faulty variant is the correct snapshot
overlaid with that variant's `files`. These are full source files, not patches.
For tests-only labs, application source is already correct. For repair/feature
labs, the starter must pass public tests but fail at least one contract assertion.

Give every lab 2–4 meaningful faulty variants. Include the seeded starter defect
among variants for repair/feature labs. The `reference_tests` suite must pass
correct code and fail each variant with a normal assertion failure. Import,
collection, fixture, syntax, and setup errors do not qualify. Use `assert` and
`pytest.raises` normally. An unconditional failure is not meaningful evidence.
Contracts must check outputs and side effects independently from implementation.

The runner grades the learner's `tests/learner/` suite against correct code and
all variants. It also checks their implementation against `contract_tests` for
repair/feature labs. Public tests must pass both starter and reference. Learner
tests must not import instructor files, inspect hidden variant names, or depend
on implementation source text. Keep contracts and reference_tests separate.

Required brief sections: context; learn first; file map (3–6 application files);
read/trace task; exact change or test assignment; allowed edit scope; explicit
accepted and rejected behavior; examples; boundary checklist tied to variant
classes; focused pytest commands; one optional AI prompt requesting explanation
or review with file evidence and no implementation; hints; technical done checks.
Teach before testing. Use short English sentences. Define unfamiliar terms.
Show a worked example, but do not reveal the assigned fix or complete tests.

Use `uv run pytest -q tests/learner` for focused learner tests. Do not write tests
in the learner scaffold; its purpose is for the learner to write them. Public
tests can demonstrate pytest syntax on a separate supported behavior. No request
to explain answers out loud, prepare stories, or perform behavioral practice.

Labs 01–04 cover a compact configuration/intake application. Lab01 focuses on
reading the pipeline and characterization tests. Lab02 adds parametrized typed
boundary checks. Lab03 fixes state leakage. Lab04 tests a caller with a fake
dependency and exception handling. Evolve familiar names where useful, but each
snapshot is independent and has exactly one central assignment.

Labs 05–06 use a compact ticket API with FastAPI TestClient. Lab05 fixes validation
before mutation. Lab06 adds one PATCH field with exact missing/null/zero rules.
Labs 07–08 use a paged client with fake clock and transport. Lab07 writes tests
for calls, stop conditions, and budgets. Lab08 reviews a supplied plausible AI
patch and fixes one regression. Include the supplied patch in the brief.

The caller should receive dependencies through a constructor or parameter where
possible. Teach patching where a symbol is looked up in at least one brief.
Do not require a learner to learn an unrelated framework feature for a small task.

Instructor checks should include diverse input classes, not many copies of a
single happy path. Explicitly calculate expected results. State what the lab
does not model. These are constructed exercises, not Capital One questions.
