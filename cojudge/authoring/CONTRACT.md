# Authoring contract

Each `pNN.py` exports a `SPEC` dictionary. Do not write generated problem files.
No packages beyond the Python standard library. Author all text in clear English.

Required fields:

```python
SPEC = {
    "number": 1,
    "slug": "strict-amounts",  # builder adds c1-01-
    "title": "Strict amounts",
    "difficulty": "Easy",  # Easy, Medium, Hard
    "time": 20,
    "prerequisites": "Lists, dictionaries, and functions.",
    "learn": "A short lesson, 80–160 words. Teach before testing.",
    "task": "Precise input/output contract as Markdown. Describe every field and error.",
    "constraints": ["..."],
    "hints": ["Conceptual hint.", "More specific hint."],
    "starter": "def solve(data):\n    raise NotImplementedError\n",
    "reference": "def solve(data):\n    return ...\n",  # full Python module; may include classes/imports
    "java": "public Object solve(Map<String,Object> d) { ... }", # complete Java method(s) INSIDE Marker
    "approach": "Reference explanation, with complexity and production limits.",
    "cases": [
        {"input": {"values": []}, "expected": [], "label": "empty batch"},
        # >= 12 distinct inputs with explicitly or independently derived expected answers
    ],
    "generated": [{"values": [1, 2]}],  # >= 12 additional distinct deterministic inputs, random.Random fixed seed allowed
    "mutations": [{"name": "rejects zero", "old": "n >= 0", "new": "n > 0"}],
    # old must occur in reference. At least one REALISTIC behavior bug rejected by cases.
    "sources": ["https://docs.python.org/3/library/typing.html"],
}
```

The builder adds `import json` and this supplied adapter to both starter and reference:

```python
class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
```

The learner edits `solve` and supplied helper classes. Inputs and results are JSON
values. `data` is always a JSON object. No actual network calls. Use integer clocks
for simulations. State valid domains; do not reject unspecified invalid inputs.
Python-only starter is intentional. The judge checks behavior, not syntax/architecture.

Java support available in inherited `Support` (do not reimplement the JSON parser):

```java
static Map<String,Object> obj(Object x);
static List<Object> arr(Object x);
static String s(Object x);
static int n(Object x);
static long lng(Object x);
static boolean isInteger(Object x); // true for JSON integer tokens, false for 1.0 / 1e0 / bool
static boolean b(Object x);
static Map<String,Object> map(Object... keyValuePairs);
static List<Object> list(Object... values);
// J.parse(String), J.dump(Object), J.equal(Object,Object) handle JSON.
```

Marker imports java.util.*, java.math.*, java.time.*, java.time.format.*,
java.util.regex.*, java.nio.charset.StandardCharsets. Add fully qualified names
for other standard classes. Use n/lng for numeric conversion.
Do not mutate data used for comparison. Return JSON-compatible structures.
JSON integer tokens use BigInteger; decimal/exponent tokens use BigDecimal.
Use isInteger(x) for Python type(x) is int validation, including 1.0 and 1e0.
Java reference computes answers independently from arbitrary valid inputs.
Do not use expected-output lookup tables or call the Python reference from Java.

At least 12 explicit cases and 12 additional distinct cases per problem.
Prefer 15–30 explicit cases and 25–50 generated cases where useful. Include empty,
singleton, boundary, repeated operations, isolation, malformed input if covered
by the contract, and plausible production failures. Do not manufacture 12 similar
cases and call that diversity. Give first three cases readable worked examples.

Mutation tests are executable string replacements in Python reference. Select a
realistic defect (wrong inequality, missing dedup, wrong ordering, shared state,
partial write). At least one per problem. They must be killed by the official tests.
Provide intentionally flawed starter code for selected bug-fix problems; explain
that it is faulty. For other problems use short stubs with useful typed signatures.

No instructor material goes to attempts. No author writes or changes existing
attempts. Do not commit: the coordinator commits coherent reviewed units and pushes.
Use `uv run python` for checks. Report actual verification and limitations.
