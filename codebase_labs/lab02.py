"""Instructor data for runtime boundary tests in an independent snapshot."""

from textwrap import dedent


CONTRACT_TESTS = dedent('''\
    import pytest
    from app.service import load_settings
    from app.validation import validate_retries


    @pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5])
    def test_all_accepted_retry_counts(value):
        result = validate_retries(value)
        assert result == value
        assert type(result) is int


    @pytest.mark.parametrize("value", [
        True, False, -1, 6, 99, "0", "4", "", 0.0, 4.5, None, [], {},
    ])
    def test_rejected_runtime_classes(value):
        with pytest.raises(ValueError):
            validate_retries(value)


    def test_settings_default_presence_and_no_mutation():
        payload = {"extra": ["untouched"]}
        assert load_settings(payload).retries == 3
        assert payload == {"extra": ["untouched"]}
        assert load_settings({"retries": 0}).retries == 0
        with pytest.raises(ValueError):
            load_settings({"retries": None})


    @pytest.mark.parametrize("value", [False, "2", 2.0, 6])
    def test_service_keeps_the_validation_boundary(value):
        payload = {"retries": value}
        with pytest.raises(ValueError):
            load_settings(payload)
        assert payload == {"retries": value}
''')

REFERENCE_TESTS = dedent('''\
    import pytest
    from app.service import load_settings
    from app.validation import validate_retries


    @pytest.mark.parametrize("value", [0, 2, 5], ids=["minimum", "middle", "maximum"])
    def test_accepts_inclusive_integer_range(value):
        result = validate_retries(value)
        assert result == value
        assert type(result) is int


    @pytest.mark.parametrize("value", [
        True, False, "2", 2.0, 2.5, -1, 6, None, [], {},
    ], ids=[
        "true", "false", "numeric-text", "whole-float", "fraction",
        "below", "above", "null", "list", "dictionary",
    ])
    def test_rejects_wrong_types_and_out_of_range_values(value):
        with pytest.raises(ValueError):
            validate_retries(value)


    def test_entry_point_distinguishes_absent_null_and_zero():
        assert load_settings({}).retries == 3
        assert load_settings({"retries": 0}).retries == 0
        with pytest.raises(ValueError):
            load_settings({"retries": None})
''')

VALIDATION = dedent('''\
    """Enforce runtime rules; annotations alone do not enforce them."""


    def validate_retries(value: int) -> int:
        if type(value) is not int or not 0 <= value <= 5:
            raise ValueError("retries must be an integer from 0 through 5")
        return value
''')

LAB = {
    "id": "lab02",
    "title": "Parameterize the runtime boundary",
    "kind": "tests",
    "after": 4,
    "minutes": 35,
    "objective": "Use parametrized tests to distinguish runtime types from type annotations.",
    "brief": dedent('''\
        ## Context

        This constructed intake snapshot loads a retry setting.
        It is not a Capital One question. It is independent of lab01.
        This snapshot has a different documented default and range.
        The application is correct. Write tests for its runtime boundary.
        This lab does not model parsing JSON, a network, or static type checking.

        ## Learn first

        A type annotation describes an intended type.
        It does not reject a value when Python calls a function.
        Runtime validation checks the actual value during execution.
        Python treats `bool` as a subclass of `int`.
        The product rule can still reject booleans.

        Work through this trace: `load_settings({"retries": 4})` reads `4`.
        `validate_retries` accepts it. `IntakeSettings` stores `4`.
        The caller can read the result through `.retries`.
        No conversion from a string or float is part of this contract.

        A parametrized test runs one test function with several named inputs.
        `@pytest.mark.parametrize("value", values)` supplies one value per case.
        Use `ids=` to give useful case names in failure reports.
        Put accepted inputs and rejected inputs in separate test functions.
        Use `pytest.raises(ValueError)` for each rejected value.
        The public test shows parametrization on two ordinary accepted values.
        Choose expected outcomes from the product rule, not from the implementation.

        ## File map

        - `app/__init__.py`: package marker.
        - `app/validation.py`: `validate_retries`, the runtime boundary.
        - `app/models.py`: `IntakeSettings`, the returned data object.
        - `app/service.py`: `load_settings`, the entry point and missing-key default.
        - `tests/test_existing.py`: a small parametrized example.
        - `tests/learner/test_task.py`: your test file.

        ## Read and trace

        Run `rg -n "retries|validate_retries" app`.
        Trace how `load_settings` calls the validator.
        Locate the default and the numeric range in their separate files.
        Predict what a type annotation does when the caller passes `"4"`.

        ## Assignment and allowed edits

        Write your own parametrized boundary tests in `tests/learner/`.
        Test the validator directly. Add a small entry-point test for key presence.
        Include both ends of the valid range and all listed rejected classes.
        Only `tests/learner/` is editable.
        Do not change application files or existing tests.

        ## Exact behavior

        `validate_retries(value)` accepts only built-in integers from `0` through `5`.
        It returns the same numeric value as a built-in integer.
        It rejects booleans, integer subclasses, floats, strings, `None`, lists,
        dictionaries, negative integers, and integers above `5` with `ValueError`.
        Error-message text is not part of the contract. No value coercion is allowed.
        Custom integer subclasses are outside the required learner test matrix.

        `load_settings(payload)` accepts a built-in dictionary.
        An absent `retries` key supplies `3`.
        A present value goes through `validate_retries`, including `None` and zero.
        The result is an `IntakeSettings` object with the validated `.retries` value.
        Unknown keys are ignored. The payload stays unchanged.
        Other payload-container types are outside scope.

        ## Examples

        - `{}` gives `.retries == 3`.
        - `{"retries": 0}` gives `.retries == 0`.
        - `{"retries": 5}` gives `.retries == 5`.
        - `{"retries": None}` raises `ValueError`.
        - `True`, `"3"`, `3.0`, `-1`, and `6` each fail direct validation.

        ## Boundary checklist

        - Boolean values detect an overly broad integer check.
        - Numeric strings detect silent text conversion.
        - Whole and fractional floats detect silent numeric conversion.
        - `5` and `6` detect an incorrect inclusive upper limit.
        - Zero, negative values, null, and containers cover other boundary classes.
        - Missing, null, and zero must be separate service cases.

        ## Commands

        Run from the new lab directory.

        ```sh
        uv run pytest -q tests/test_existing.py
        uv run pytest --collect-only -q tests/learner
        uv run pytest -q tests/learner
        uv run pytest -q tests/learner -k rejects
        uv run pytest -q
        git diff -- app tests/learner
        ```

        Inspect the collected case names before running the suite.
        Read an assertion failure to find the smallest input that breaks a rule.
        New untracked test files need direct file review as well as `git diff`.

        ## Optional AI review

        "Review my boundary table against app/validation.py and app/service.py.
        Cite the file and function for each rule. Identify one missing input class.
        Do not write tests or implementation. I will write all code."

        Constructed AI claim to check: "The annotation `value: int` and
        `isinstance(value, int)` together ensure that boolean values are rejected."

        ## Hints

        First, classify each input by runtime type before checking its numeric value.
        Next, choose values just inside and just outside the range.
        Finally, verify that your rejection cases actually execute the call.
        Do not use `xfail` for behavior that the contract requires.

        ## Done checks

        Accepted cases assert values and output types.
        Rejected cases assert `ValueError`.
        Your suite has separate boolean, text, float, and range cases.
        Correct code passes. Each faulty validator causes an assertion failure.
        A test count does not show that all boundary classes are covered.
    '''),
    "editable": ["tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/validation.py": VALIDATION,
        "app/models.py": dedent('''\
            from dataclasses import dataclass


            @dataclass(frozen=True)
            class IntakeSettings:
                retries: int
        '''),
        "app/service.py": dedent('''\
            from app.models import IntakeSettings
            from app.validation import validate_retries


            def load_settings(payload: dict) -> IntakeSettings:
                value = payload.get("retries", 3)
                return IntakeSettings(retries=validate_retries(value))
        '''),
        "tests/test_existing.py": dedent('''\
            import pytest
            from app.service import load_settings


            @pytest.mark.parametrize("value", [1, 3])
            def test_ordinary_retry_setting(value):
                assert load_settings({"retries": value}).retries == value
        '''),
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {
            "name": "booleans pass as integers",
            "files": {"app/validation.py": VALIDATION.replace(
                "type(value) is not int", "not isinstance(value, int)",
            )},
        },
        {
            "name": "numeric strings are coerced",
            "files": {"app/validation.py": VALIDATION.replace(
                '    if type(value) is not int',
                '    if isinstance(value, str) and value.isdigit():\n        value = int(value)\n    if type(value) is not int',
            )},
        },
        {
            "name": "floats are coerced to integers",
            "files": {"app/validation.py": VALIDATION.replace(
                '    if type(value) is not int',
                '    if isinstance(value, float):\n        value = int(value)\n    if type(value) is not int',
            )},
        },
        {
            "name": "upper boundary admits six",
            "files": {"app/validation.py": VALIDATION.replace(
                "not 0 <= value <= 5", "not 0 <= value <= 6",
            )},
        },
    ],
    "ai_claim": "The annotation value: int and isinstance(value, int) together ensure that boolean values are rejected.",
    "ai_answer": "False. An annotation does not enforce runtime validation. isinstance(True, int) is True, and True compares as 1. The input True must raise ValueError under this contract. A test with the numeric value 1 cannot detect this defect.",
    "sources": [
        "https://docs.pytest.org/en/stable/how-to/parametrize.html",
        "https://docs.python.org/3/library/stdtypes.html#boolean-type-bool",
    ],
}
