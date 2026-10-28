"""Apply explicit expiry times to a per-call cache."""

CASES = [
    {"label": "value is available before expiry", "input": {"operations": [{"op": "put", "key": "a", "value": "ready", "now": 5, "ttl": 3}, {"op": "get", "key": "a", "now": 7}]}, "expected": [None, {"hit": True, "value": "ready"}]},
    {"label": "entry expires exactly at its deadline", "input": {"operations": [{"op": "put", "key": "a", "value": 9, "now": 5, "ttl": 3}, {"op": "get", "key": "a", "now": 8}]}, "expected": [None, {"hit": False, "value": None}]},
    {"label": "cached null is distinct from a miss", "input": {"operations": [{"op": "put", "key": "a", "value": None, "now": 0, "ttl": 1}, {"op": "get", "key": "a", "now": 0}, {"op": "get", "key": "missing", "now": 0}]}, "expected": [None, {"hit": True, "value": None}, {"hit": False, "value": None}]},
    {"label": "empty operation list", "input": {"operations": []}, "expected": []},
    {"label": "get from an empty cache", "input": {"operations": [{"op": "get", "key": "a", "now": 0}]}, "expected": [{"hit": False, "value": None}]},
    {"label": "zero TTL is already expired", "input": {"operations": [{"op": "put", "key": "a", "value": 3, "now": 2, "ttl": 0}, {"op": "get", "key": "a", "now": 2}]}, "expected": [None, {"hit": False, "value": None}]},
    {"label": "replacement can shorten expiry", "input": {"operations": [{"op": "put", "key": "a", "value": "old", "now": 0, "ttl": 100}, {"op": "put", "key": "a", "value": "new", "now": 1, "ttl": 1}, {"op": "get", "key": "a", "now": 1}, {"op": "get", "key": "a", "now": 2}]}, "expected": [None, None, {"hit": True, "value": "new"}, {"hit": False, "value": None}]},
    {"label": "put replaces an expired entry", "input": {"operations": [{"op": "put", "key": "a", "value": 1, "now": 0, "ttl": 1}, {"op": "put", "key": "a", "value": 2, "now": 2, "ttl": 3}, {"op": "get", "key": "a", "now": 4}]}, "expected": [None, None, {"hit": True, "value": 2}]},
    {"label": "all falsy JSON values can be cached", "input": {"operations": [{"op": "put", "key": "false", "value": False, "now": 0, "ttl": 2}, {"op": "put", "key": "zero", "value": 0, "now": 0, "ttl": 2}, {"op": "put", "key": "text", "value": "", "now": 0, "ttl": 2}, {"op": "put", "key": "list", "value": [], "now": 0, "ttl": 2}, {"op": "put", "key": "object", "value": {}, "now": 0, "ttl": 2}, {"op": "get", "key": "false", "now": 1}, {"op": "get", "key": "zero", "now": 1}, {"op": "get", "key": "text", "now": 1}, {"op": "get", "key": "list", "now": 1}, {"op": "get", "key": "object", "now": 1}]}, "expected": [None, None, None, None, None, {"hit": True, "value": False}, {"hit": True, "value": 0}, {"hit": True, "value": ""}, {"hit": True, "value": []}, {"hit": True, "value": {}}]},
    {"label": "empty key holds a nested JSON value", "input": {"operations": [{"op": "put", "key": "", "value": {"rows": [None, True, {"n": 4.5}]}, "now": 0, "ttl": 1}, {"op": "get", "key": "", "now": 0}]}, "expected": [None, {"hit": True, "value": {"rows": [None, True, {"n": 4.5}]}}]},
    {"label": "keys are case sensitive", "input": {"operations": [{"op": "put", "key": "a", "value": 1, "now": 0, "ttl": 3}, {"op": "put", "key": "A", "value": 2, "now": 0, "ttl": 3}, {"op": "get", "key": "a", "now": 1}, {"op": "get", "key": "A", "now": 1}]}, "expected": [None, None, {"hit": True, "value": 1}, {"hit": True, "value": 2}]},
    {"label": "keys have independent deadlines", "input": {"operations": [{"op": "put", "key": "a", "value": 1, "now": 0, "ttl": 1}, {"op": "put", "key": "b", "value": 2, "now": 0, "ttl": 3}, {"op": "get", "key": "a", "now": 1}, {"op": "get", "key": "b", "now": 1}]}, "expected": [None, None, {"hit": False, "value": None}, {"hit": True, "value": 2}]},
    {"label": "reads do not extend the deadline", "input": {"operations": [{"op": "put", "key": "a", "value": "x", "now": 10, "ttl": 2}, {"op": "get", "key": "a", "now": 11}, {"op": "get", "key": "a", "now": 12}, {"op": "get", "key": "a", "now": 13}]}, "expected": [None, {"hit": True, "value": "x"}, {"hit": False, "value": None}, {"hit": False, "value": None}]},
    {"label": "same-time writes use the last value", "input": {"operations": [{"op": "put", "key": "a", "value": "first", "now": 2, "ttl": 2}, {"op": "put", "key": "a", "value": "last", "now": 2, "ttl": 2}, {"op": "get", "key": "a", "now": 2}]}, "expected": [None, None, {"hit": True, "value": "last"}]},
    {"label": "expiry arithmetic exceeds fixed-width integers", "input": {"operations": [{"op": "put", "key": "a", "value": 7, "now": 18446744073709551616, "ttl": 18446744073709551616}, {"op": "get", "key": "a", "now": 36893488147419103231}, {"op": "get", "key": "a", "now": 36893488147419103232}]}, "expected": [None, {"hit": True, "value": 7}, {"hit": False, "value": None}]},
    {"label": "zero TTL replacement discards a live value", "input": {"operations": [{"op": "put", "key": "a", "value": "old", "now": 0, "ttl": 20}, {"op": "put", "key": "a", "value": "new", "now": 1, "ttl": 0}, {"op": "get", "key": "a", "now": 1}]}, "expected": [None, None, {"hit": False, "value": None}]},
]

SPEC = {
    "number": 11,
    "slug": "expire-cache-entries",
    "title": "Apply cache expiry without using the clock",
    "difficulty": "Medium",
    "category": "03-stateful-services",
    "ticket": "The cache must distinguish cached null values from misses and expire entries at the exact deadline.",
    "task": "Implement `run_cache(operations)`. Process operations in order with an initially empty cache. A put is `{'op': 'put', 'key': STRING, 'value': JSON_VALUE, 'now': INTEGER, 'ttl': INTEGER}`. Store the value with expiry `now + ttl`, replacing any value and deadline for that key. Append null to the output. A get is `{'op': 'get', 'key': STRING, 'now': INTEGER}`. If the key exists and `now < expiry`, append `{'hit': true, 'value': STORED_VALUE}`. Otherwise append `{'hit': false, 'value': null}`. A stored null is a hit before expiry. A zero TTL expires immediately. Gets do not change expiry. Return one result per operation in input order. Keys are ASCII strings and can be empty. Times are nonnegative integers in nondecreasing order; TTLs are nonnegative integers. Compare keys exactly. Each call starts empty. Do not use the wall clock or impose a capacity. Do not change the input.",
    "constraints": ["Operations are put or get and contain all fields specified for that operation.", "Values can be any JSON value, including null, false, zero, empty containers, and nested objects.", "now and ttl are integers greater than or equal to zero; booleans are not times.", "There is no fixed maximum integer time."],
    "function": "run_cache",
    "starter": "def run_cache(operations):\n    raise NotImplementedError\n",
    "reference": '''def run_cache(operations):
    entries = {}
    results = []
    for operation in operations:
        key, now = operation["key"], operation["now"]
        if operation["op"] == "put":
            entries[key] = (operation["value"], now + operation["ttl"])
            results.append(None)
        else:
            entry = entries.get(key)
            if entry is not None and now < entry[1]:
                results.append({"hit": True, "value": entry[0]})
            else:
                results.append({"hit": False, "value": None})
    return results
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Map<String,Object>> entries = new HashMap<>();
    List<Object> results = new ArrayList<>();
    for (Object raw : arr(d.get("operations"))) {
        Map<String,Object> operation = obj(raw);
        String key = s(operation.get("key"));
        BigInteger now = new BigInteger(operation.get("now").toString());
        if (s(operation.get("op")).equals("put")) {
            BigInteger ttl = new BigInteger(operation.get("ttl").toString());
            entries.put(key, map("value", operation.get("value"), "expires", now.add(ttl)));
            results.add(null);
        } else {
            Map<String,Object> entry = entries.get(key);
            if (entry != null && now.compareTo((BigInteger) entry.get("expires")) < 0) {
                results.add(map("hit", true, "value", entry.get("value")));
            } else {
                results.add(map("hit", false, "value", null));
            }
        }
    }
    return results;
}''',
    "cases": CASES,
    "mutations": [
        {"name": "keep values at the expiry deadline", "old": "now < entry[1]", "new": "now <= entry[1]"},
        {"name": "treat falsy cached values as misses", "old": "if entry is not None and now < entry[1]:", "new": "if entry is not None and entry[0] and now < entry[1]:"},
        {"name": "preserve the first write instead of replacing", "old": 'entries[key] = (operation["value"], now + operation["ttl"])', "new": 'entries.setdefault(key, (operation["value"], now + operation["ttl"]))'},
        {"name": "use TTL as an absolute deadline", "old": 'now + operation["ttl"]', "new": 'operation["ttl"]'},
    ],
}

# Bound decimal precision so Python and the independent marker preserve the same JSON value.
SPEC["constraints"].append("Floating-point values have at most six decimal places and an absolute value at most 1000000.")
SPEC["cases"].append({'input': {'operations': [{'op': 'put', 'key': 'decimal', 'value': [1e-06, -999999.999999], 'now': 0, 'ttl': 1}, {'op': 'get', 'key': 'decimal', 'now': 0}]}, 'expected': [None, {'hit': True, 'value': [1e-06, -999999.999999]}], 'label': 'decimal value boundaries'})
