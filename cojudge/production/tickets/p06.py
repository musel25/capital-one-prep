"""Apply a flat settings patch with explicit null deletion."""

CASES = [
    {"input": {"settings": {"theme": "dark", "lang": "en"}, "patch": {"theme": "light"}}, "expected": {"theme": "light", "lang": "en"}, "label": "replace one setting and preserve another"},
    {"input": {"settings": {"theme": "dark"}, "patch": {"theme": None}}, "expected": {}, "label": "null removes an existing key"},
    {"input": {"settings": {}, "patch": {}}, "expected": {}, "label": "both objects empty"},
    {"input": {"settings": {"a": 1}, "patch": {}}, "expected": {"a": 1}, "label": "empty patch preserves settings"},
    {"input": {"settings": {}, "patch": {"a": 1}}, "expected": {"a": 1}, "label": "add to empty settings"},
    {"input": {"settings": {"a": 1}, "patch": {"missing": None}}, "expected": {"a": 1}, "label": "removing a missing key is a no-op"},
    {"input": {"settings": {"enabled": True}, "patch": {"enabled": False}}, "expected": {"enabled": False}, "label": "false is a replacement value"},
    {"input": {"settings": {"count": 8}, "patch": {"count": 0}}, "expected": {"count": 0}, "label": "zero is a replacement value"},
    {"input": {"settings": {"name": "old"}, "patch": {"name": ""}}, "expected": {"name": ""}, "label": "empty string is a replacement value"},
    {"input": {"settings": {"options": [1]}, "patch": {"options": []}}, "expected": {"options": []}, "label": "empty list replaces a value"},
    {"input": {"settings": {"config": {"a": 1, "b": 2}}, "patch": {"config": {"b": None}}}, "expected": {"config": {"b": None}}, "label": "nested object replaces the whole value"},
    {"input": {"settings": {"x": None, "keep": None}, "patch": {"x": "set", "new": None}}, "expected": {"x": "set", "keep": None}, "label": "unpatched null values remain"},
    {"input": {"settings": {"a": 1, "b": 2, "c": 3}, "patch": {"a": None, "b": 0, "d": [True, None]}}, "expected": {"b": 0, "c": 3, "d": [True, None]}, "label": "delete replace and add in one patch"},
    {"input": {"settings": {"Mode": 1, "mode": 2, "": 3}, "patch": {"Mode": None, "": {}}}, "expected": {"mode": 2, "": {}}, "label": "keys are exact and may be empty"},
]

SPEC = {
    "number": 6,
    "slug": "flat-settings-patch",
    "title": "Apply a settings patch",
    "difficulty": "Easy",
    "category": "01-data-and-api",
    "ticket": "The settings endpoint must distinguish deletion from valid false, zero and empty replacement values.",
    "task": "Implement apply_settings_patch(settings, patch). Both arguments are JSON objects with string keys and arbitrary JSON values. Return a new settings object. Start with all existing entries. For each patch entry, remove the key if its value is null. Removing an absent key does nothing. Otherwise set the key to that value, replacing any existing value. Apply these rules only at the top level: nested objects and lists replace entire values, and null inside a nested value is retained. Unpatched entries remain unchanged, including existing null values. Keys are case-sensitive and may be empty strings. Do not change settings, patch or their nested values. An empty patch still returns a new object. Each call is independent.",
    "constraints": ["Each top-level object contains 0–200 keys.", "All values are valid JSON values; objects are not merged recursively.", "Inputs satisfy the contract. No input validation or external storage is required."],
    "function": "apply_settings_patch",
    "starter": "def apply_settings_patch(settings, patch):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''def apply_settings_patch(settings, patch):
    result = settings.copy()
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value
    return result
'''

SPEC["java"] = '''public Object solve(Map<String,Object> d) {
    Map<String,Object> result = new LinkedHashMap<>(obj(d.get("settings")));
    for (Map.Entry<String,Object> entry : obj(d.get("patch")).entrySet()) {
        if (entry.getValue() == null) result.remove(entry.getKey());
        else result.put(entry.getKey(), entry.getValue());
    }
    return result;
}
'''

SPEC["mutations"] = [
    {"name": "delete false zero and empty values", "old": 'if value is None:', "new": 'if not value:'},
    {"name": "store null instead of deleting", "old": 'result.pop(key, None)', "new": 'result[key] = None'},
    {"name": "reject deletion of a missing key", "old": 'result.pop(key, None)', "new": 'result.pop(key)'},
    {"name": "discard unpatched settings", "old": 'result = settings.copy()', "new": 'result = {}'},
]

# Bound decimal precision so Python and the independent marker preserve the same JSON value.
SPEC["constraints"].append("Floating-point values have at most six decimal places and an absolute value at most 1000000.")
SPEC["cases"].append({'input': {'settings': {'small': 1e-06, 'large': -999999.999999}, 'patch': {}}, 'expected': {'small': 1e-06, 'large': -999999.999999}, 'label': 'decimal value boundaries'})
