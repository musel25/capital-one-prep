"""Remove secret values from nested JSON logs."""

CASES = [
    {"input": {"value": {"user": "sam", "password": "abc"}}, "expected": {"user": "sam", "password": "[REDACTED]"}, "label": "redact a top-level password"},
    {"input": {"value": {"Token": "abc", "SECRET": None}}, "expected": {"Token": "[REDACTED]", "SECRET": "[REDACTED]"}, "label": "case-insensitive secret key matching"},
    {"input": {"value": {"profile": {"password": "abc"}, "events": [{"token": 42}, "ok"]}}, "expected": {"profile": {"password": "[REDACTED]"}, "events": [{"token": "[REDACTED]"}, "ok"]}, "label": "recurse through objects and arrays"},
    {"input": {"value": {}}, "expected": {}, "label": "empty object"},
    {"input": {"value": []}, "expected": [], "label": "empty array"},
    {"input": {"value": None}, "expected": None, "label": "null root"},
    {"input": {"value": "password"}, "expected": "password", "label": "scalar text is not a secret key"},
    {"input": {"value": [False, 0, 3.5, "token", None]}, "expected": [False, 0, 3.5, "token", None], "label": "preserve scalar types and values"},
    {"input": {"value": {"password": {"safe": [1, 2]}, "secret": [1, {"x": 2}]}}, "expected": {"password": "[REDACTED]", "secret": "[REDACTED]"}, "label": "replace a secret's entire subtree"},
    {"input": {"value": {"password_hint": "keep", "access_token": "keep", "secrets": "keep", " token": "keep"}}, "expected": {"password_hint": "keep", "access_token": "keep", "secrets": "keep", " token": "keep"}, "label": "match whole keys without trimming"},
    {"input": {"value": [[{"pAsSwOrD": False}], {"x": [{"ToKeN": 0}]}]}, "expected": [[{"pAsSwOrD": "[REDACTED]"}], {"x": [{"ToKeN": "[REDACTED]"}]}], "label": "false and zero secrets still redact"},
    {"input": {"value": {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"secret": "deep"}}}}}}}}}}, "expected": {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"secret": "[REDACTED]"}}}}}}}}}, "label": "deep secret within the supported depth"},
    {"input": {"value": {"password": "[REDACTED]", "note": "[REDACTED]"}}, "expected": {"password": "[REDACTED]", "note": "[REDACTED]"}, "label": "already redacted content is stable"},
    {"input": {"value": {"": {"secret": ""}, "PASSWORD": [], "secret": {}}}, "expected": {"": {"secret": "[REDACTED]"}, "PASSWORD": "[REDACTED]", "secret": "[REDACTED]"}, "label": "empty keys and empty secret values"},
]

SPEC = {
    "number": 7,
    "slug": "nested-secret-redaction",
    "title": "Redact secrets from JSON logs",
    "difficulty": "Medium",
    "category": "02-clients-and-reliability",
    "ticket": "The request logger must remove secret values from nested payloads before it writes them.",
    "task": "Implement redact_secrets(value) for any JSON value. For each object key, compare its ASCII letters without regard to case. If the whole key equals password, token or secret, replace its entire value with the string '[REDACTED]'. Preserve the original key spelling. Do not inspect that replaced subtree. Recursively process values under all other object keys and every list element. Return scalar values unchanged, including strings that contain secret words. Matching does not trim whitespace or match substrings. Empty objects and lists remain empty. Do not change the input tree. Repeated calls must be independent and redacting an already redacted result must leave its JSON value unchanged.",
    "constraints": ["The input is a valid JSON tree with ASCII object keys.", "The maximum nesting depth is 10 and the tree has at most 1000 nodes.", "Inputs satisfy the contract. No input validation, file access or network calls are required."],
    "function": "redact_secrets",
    "starter": "def redact_secrets(value):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''def redact_secrets(value):
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in {"password", "token", "secret"}
            else redact_secrets(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    return value
'''

SPEC["java"] = '''private Object redact(Object value) {
    if (value instanceof Map) {
        Map<String,Object> result = new LinkedHashMap<>();
        for (Map.Entry<String,Object> entry : obj(value).entrySet()) {
            String lower = entry.getKey().toLowerCase(Locale.ROOT);
            boolean secret = lower.equals("password") || lower.equals("token") || lower.equals("secret");
            result.put(entry.getKey(), secret ? "[REDACTED]" : redact(entry.getValue()));
        }
        return result;
    }
    if (value instanceof List) {
        List<Object> result = new ArrayList<>();
        for (Object item : arr(value)) result.add(redact(item));
        return result;
    }
    return value;
}

public Object solve(Map<String,Object> d) {
    return redact(d.get("value"));
}
'''

SPEC["mutations"] = [
    {"name": "match secret keys case-sensitively", "old": 'key.lower() in', "new": 'key in'},
    {"name": "skip objects within arrays", "old": 'return [redact_secrets(item) for item in value]', "new": 'return list(value)'},
    {"name": "leave nested object values unchanged", "old": 'else redact_secrets(item)', "new": 'else item'},
    {"name": "trim key whitespace before matching", "old": 'key.lower() in', "new": 'key.strip().lower() in'},
    {"name": "forget token keys", "old": '{"password", "token", "secret"}', "new": '{"password", "secret"}'},
]

# Bound decimal precision so Python and the independent marker preserve the same JSON value.
SPEC["constraints"].append("Floating-point values have at most six decimal places and an absolute value at most 1000000.")
SPEC["cases"].append({'input': {'value': [1e-06, -999999.999999]}, 'expected': [1e-06, -999999.999999], 'label': 'decimal value boundaries'})
