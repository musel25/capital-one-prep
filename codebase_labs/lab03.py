"""Instructor data for the shared-state repair lab."""

from textwrap import dedent


CONTRACT_TESTS = dedent('''\
    import pytest
    from app.queue import IntakeQueue
    from app.service import record


    def test_existing_instances_have_separate_histories():
        first = IntakeQueue("west")
        second = IntakeQueue("east")
        assert record(first, " alpha ") == {"owner": "west", "labels": ["alpha"]}
        assert second.snapshot() == {"owner": "east", "labels": []}
        record(second, "beta")
        record(first, "alpha")
        assert first.snapshot() == {"owner": "west", "labels": ["alpha", "alpha"]}
        assert second.snapshot() == {"owner": "east", "labels": ["beta"]}


    def test_construction_cannot_erase_an_existing_history():
        original = IntakeQueue("same")
        record(original, "saved")
        later = IntakeQueue("same")
        assert original.snapshot() == {"owner": "same", "labels": ["saved"]}
        assert later.snapshot() == {"owner": "same", "labels": []}


    def test_snapshot_is_detached_from_live_state_in_both_directions():
        queue = IntakeQueue("desk")
        record(queue, "one")
        earlier = queue.snapshot()
        earlier["owner"] = "changed"
        earlier["labels"].append("outside")
        assert queue.snapshot() == {"owner": "desk", "labels": ["one"]}
        record(queue, "two")
        assert earlier == {"owner": "changed", "labels": ["one", "outside"]}
        assert queue.snapshot() == {"owner": "desk", "labels": ["one", "two"]}


    @pytest.mark.parametrize("label", ["", " \t ", None, 4])
    def test_invalid_add_preserves_history(label):
        queue = IntakeQueue("review")
        record(queue, "keep")
        with pytest.raises(ValueError):
            record(queue, label)
        assert queue.snapshot() == {"owner": "review", "labels": ["keep"]}


    def test_owner_uses_the_same_text_boundary():
        assert IntakeQueue("  NORTH ").snapshot() == {"owner": "NORTH", "labels": []}
        with pytest.raises(ValueError):
            IntakeQueue(" ")
''')

REFERENCE_TESTS = dedent('''\
    import pytest
    from app.queue import IntakeQueue
    from app.service import record


    def test_two_existing_queues_do_not_share_labels():
        left = IntakeQueue("left")
        right = IntakeQueue("right")
        record(left, "red")
        assert right.snapshot() == {"owner": "right", "labels": []}
        record(right, "blue")
        assert left.snapshot() == {"owner": "left", "labels": ["red"]}
        assert right.snapshot() == {"owner": "right", "labels": ["blue"]}


    def test_new_queue_does_not_clear_old_queue():
        first = IntakeQueue("desk")
        record(first, "keep")
        new = IntakeQueue("desk")
        assert first.snapshot() == {"owner": "desk", "labels": ["keep"]}
        assert new.snapshot() == {"owner": "desk", "labels": []}


    def test_snapshot_edits_do_not_change_the_queue():
        queue = IntakeQueue("owner")
        record(queue, "first")
        result = queue.snapshot()
        result["labels"].append("external")
        assert queue.snapshot() == {"owner": "owner", "labels": ["first"]}
        record(queue, "second")
        assert result["labels"] == ["first", "external"]


    def test_rejection_preserves_earlier_labels_and_order():
        queue = IntakeQueue("owner")
        record(queue, " one ")
        record(queue, "two")
        record(queue, "one")
        with pytest.raises(ValueError):
            record(queue, " ")
        assert queue.snapshot() == {"owner": "owner", "labels": ["one", "two", "one"]}
''')

STARTER_QUEUE = dedent('''\
    """Keep the labels for one intake owner."""
    from app.validation import clean_text


    class IntakeQueue:
        _labels: list[str] = []

        def __init__(self, owner: str):
            self.owner = clean_text(owner)

        def add(self, label: str) -> None:
            cleaned = clean_text(label)
            self._labels.append(cleaned)

        def snapshot(self) -> dict:
            return {"owner": self.owner, "labels": list(self._labels)}
''')

CORRECT_QUEUE = dedent('''\
    """Keep the labels for one intake owner."""
    from app.validation import clean_text


    class IntakeQueue:
        def __init__(self, owner: str):
            self.owner = clean_text(owner)
            self._labels: list[str] = []

        def add(self, label: str) -> None:
            cleaned = clean_text(label)
            self._labels.append(cleaned)

        def snapshot(self) -> dict:
            return {"owner": self.owner, "labels": list(self._labels)}
''')

LAB = {
    "id": "lab03",
    "title": "Repair state leakage between queues",
    "kind": "repair",
    "after": 8,
    "minutes": 45,
    "objective": "Write a regression test and repair ownership of mutable instance state.",
    "brief": dedent('''\
        ## Context

        This is a constructed exercise. It is not a Capital One question.
        Each intake queue belongs to one owner and holds that owner's labels.
        The starter passes the public test. It has a disclosed state-isolation defect.
        Operations on one queue can affect another queue.
        This independent snapshot does not model threads, persistence, or shared queues.

        ## Learn first

        State is data that remains between method calls.
        A mutable object can change after it is created. A list is mutable.
        An instance is one object created from a class.
        A class attribute can be shared by all instances.
        An instance attribute belongs to one instance.
        Two different attribute names can still refer to the same list.

        A regression test reproduces a defect before the repair.
        It then protects the repaired behavior.
        Write that test first. Confirm an assertion failure before editing the source.

        Work through a correct single-queue example.
        `queue = IntakeQueue(" desk ")` creates owner `"desk"` with no labels.
        `record(queue, " draft ")` returns `{"owner": "desk", "labels": ["draft"]}`.
        A second record of `"draft"` keeps both entries.
        This example does not prove that two queues are independent.

        A snapshot is a returned view of state at one time.
        This contract requires a detached dictionary and a detached labels list.
        A shallow list copy is sufficient here because each label is a string.
        This rule would need more analysis if labels contained mutable nested data.

        ## File map

        - `app/__init__.py`: package marker.
        - `app/validation.py`: `clean_text`, required text validation.
        - `app/queue.py`: `IntakeQueue`, label ownership and snapshots.
        - `app/service.py`: `record`, the public composition of add and snapshot.
        - `tests/test_existing.py`: the supported single-queue path.
        - `tests/learner/test_task.py`: your regression and compatibility tests.

        ## Read and trace

        Run `rg -n "class |def |labels|clean_text" app`.
        Trace `record` through `add` and `snapshot`.
        Find every place where a labels list is created, changed, or returned.
        Predict the results for two queues before you run your regression.
        Test two live instances in one test. Separate tests can hide their relationship.

        ## Assignment and allowed edits

        Write a failing regression in `tests/learner/` before the repair.
        Repair state ownership only in `app/queue.py`.
        Preserve validation, order, duplicates, and detached snapshots.
        Do not change method names, parameters, return shapes, or the other app files.
        Do not clear global state in test setup to hide leakage.
        Do not edit the public tests or runner files.

        ## Exact behavior

        `IntakeQueue(owner)` starts with an empty history for that instance.
        An owner must be a string with text after stripping outside whitespace.
        Store the stripped owner. Preserve its case.
        Missing text, non-string values, and whitespace-only text raise `ValueError`.
        Error-message text is not part of the contract.

        `add(label)` applies the same text rule to a label.
        A valid call appends one stripped label and returns `None`.
        Preserve insertion order and duplicates. Preserve case.
        A rejected call raises `ValueError` and leaves state unchanged.
        `snapshot()` returns exactly `{"owner": <owner>, "labels": <list>}`.
        Editing a returned dictionary or list must not change the queue.
        Later queue changes must not change an earlier snapshot.
        Constructing or changing any queue must not change another queue.
        This also applies when two queues have the same owner text.
        `record(queue, label)` adds the label and returns the resulting snapshot.

        ## Examples

        - Two new queues each start with `labels == []`.
        - Add `"red"` to the first. The second still has `labels == []`.
        - Create a third queue. The first still has `labels == ["red"]`.
        - Change a returned list. A new snapshot still shows the queue's own labels.
        - Add `" "`. The call raises `ValueError` and preserves the previous history.

        ## Boundary checklist

        - Two existing queues with interleaved writes detect shared state.
        - Creating a later queue detects a repair that clears a shared list.
        - Editing a returned list detects a snapshot that exposes live state.
        - Repeated labels and rejected additions protect existing behavior.

        ## Pytest lesson and commands

        Keep arrange, act, and assert visible in each test.
        Arrange means create the input objects. Act means call the application.
        Assert means compare the observed result with an independent prediction.
        A function-scoped fixture creates fresh test data for each test.
        You may use a fixture for repeated setup, but do not hide the two-queue scenario.

        Run from the new lab directory.

        ```sh
        uv run pytest -q tests/test_existing.py
        uv run pytest --collect-only -q tests/learner
        uv run pytest -q tests/learner
        uv run pytest -q tests/learner -k queue
        uv run pytest -q
        git diff -- app/queue.py tests/learner
        ```

        Run the focused suite before and after the repair.
        Record the failing test name and actual output in your test-file docstring.
        New untracked files may need direct review because `git diff` omits them.

        ## Optional AI review

        "Review my regression and my diff for state ownership. Cite the file,
        class, and method behind each concern. Check whether two live instances
        can still affect each other. Do not write the fix or tests. I will write all code."

        Constructed AI claim to check: "Clearing the labels list in `__init__`
        gives every new queue a clean list, so it fixes state isolation."

        ## Hints

        First, inspect where the list is allocated.
        Next, compare construction before a write with construction after a write.
        Finally, check ownership at the snapshot boundary as well as the instance boundary.

        ## Done checks

        Your own regression failed by assertion before the repair.
        It passes after the repair. Public tests also pass.
        The checker accepts the behavior and rejects all faulty variants with your tests.
        Your diff changes only queue ownership and your test files.
        No test depends on another test running first.
    '''),
    "editable": ["app/queue.py", "tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/validation.py": dedent('''\
            def clean_text(value: object) -> str:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("text must be a nonblank string")
                return value.strip()
        '''),
        "app/queue.py": STARTER_QUEUE,
        "app/service.py": dedent('''\
            from app.queue import IntakeQueue


            def record(queue: IntakeQueue, label: str) -> dict:
                queue.add(label)
                return queue.snapshot()
        '''),
        "tests/test_existing.py": dedent('''\
            from app.queue import IntakeQueue
            from app.service import record


            def test_record_trims_the_latest_label():
                queue = IntakeQueue(" public ")
                result = record(queue, " draft ")
                assert result["owner"] == "public"
                assert result["labels"][-1] == "draft"
        '''),
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {"app/queue.py": CORRECT_QUEUE},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {"name": "seeded shared class list", "files": {"app/queue.py": STARTER_QUEUE}},
        {
            "name": "new instance clears the shared list",
            "files": {"app/queue.py": STARTER_QUEUE.replace(
                "        self.owner = clean_text(owner)",
                "        self.owner = clean_text(owner)\n        self._labels.clear()",
            )},
        },
        {
            "name": "snapshot exposes the owned list",
            "files": {"app/queue.py": CORRECT_QUEUE.replace(
                '"labels": list(self._labels)', '"labels": self._labels',
            )},
        },
    ],
    "ai_claim": "Clearing the labels list in __init__ gives every new queue a clean list, so it fixes state isolation.",
    "ai_answer": "False. Create queue A, record 'saved', then create queue B. If construction clears one shared list, A loses 'saved'. If both queues exist before either write, they also still share later writes. Ownership must be separate; clearing shared data does not make it separate.",
    "sources": [
        "https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables",
        "https://docs.pytest.org/en/stable/how-to/fixtures.html",
    ],
}
