"""Keep the latest value for each event entity."""


def case(events, expected, label):
    return {"input": {"events": events}, "expected": expected, "label": label}


CASES = [
    case([], {}, "empty event stream"),
    case([{"entity": "a", "version": 1, "value": "first"}], {"a": "first"}, "one entity"),
    case([{"entity": "a", "version": 1, "value": "old"},
          {"entity": "a", "version": 2, "value": "new"}], {"a": "new"}, "new version replaces value"),
    case([{"entity": "a", "version": 2, "value": "new"},
          {"entity": "a", "version": 1, "value": "old"}], {"a": "new"}, "late old event is ignored"),
    case([{"entity": "a", "version": 4, "value": "first"},
          {"entity": "a", "version": 4, "value": "second"}], {"a": "first"}, "first equal version wins"),
    case([{"entity": "a", "version": 9, "value": 1},
          {"entity": "b", "version": 1, "value": 2}], {"a": 1, "b": 2}, "versions are local to each entity"),
    case([{"entity": "a", "version": 1, "value": 7},
          {"entity": "a", "version": 2, "value": None}], {"a": None}, "null replaces a value"),
    case([{"entity": "a", "version": 1, "value": True},
          {"entity": "a", "version": 2, "value": False}], {"a": False}, "false is a stored value"),
    case([{"entity": "a", "version": 1, "value": 10},
          {"entity": "a", "version": 3, "value": 0}], {"a": 0}, "zero is a stored value"),
    case([{"entity": "a", "version": 1, "value": ""},
          {"entity": "b", "version": 1, "value": []},
          {"entity": "c", "version": 1, "value": {}}],
         {"a": "", "b": [], "c": {}}, "empty JSON values"),
    case([{"entity": "a", "version": 1, "value": {"rows": [1, None, {"ok": True}]}},
          {"entity": "a", "version": 1, "value": {"rows": []}}],
         {"a": {"rows": [1, None, {"ok": True}]}}, "nested value survives equal version"),
    case([{"entity": "A", "version": 1, "value": 1},
          {"entity": "a", "version": 1, "value": 2},
          {"entity": "a b", "version": 1, "value": 3}],
         {"A": 1, "a": 2, "a b": 3}, "entity names are exact"),
    case([{"entity": "x", "version": 5, "value": "five"},
          {"entity": "y", "version": 2, "value": "two"},
          {"entity": "x", "version": 3, "value": "three"},
          {"entity": "y", "version": 8, "value": "eight"},
          {"entity": "x", "version": 7, "value": "seven"},
          {"entity": "y", "version": 8, "value": "duplicate"}],
         {"x": "seven", "y": "eight"}, "interleaved stale and equal versions"),
    case([{"entity": "max", "version": 1000000000, "value": -4.5},
          {"entity": "max", "version": 999999999, "value": 7}],
         {"max": -4.5}, "largest allowed version"),
]

CASES = CASES[2:5] + CASES[:2] + CASES[5:]

SPEC = {
    "number": 13,
    "slug": "latest-event-values",
    "title": "Keep the latest event values",
    "difficulty": "Medium",
    "category": "03-stateful-services",
    "ticket": "A consumer must ignore stale events and retain the latest value for each entity.",
    "task": "Implement `latest_events(events)`. Each event has `entity`, `version`, and `value`. "
            "Process events in input order. Store the first event for each entity. Replace its value "
            "only when a later event has a strictly greater version. The first event wins when "
            "versions are equal. Return an object that maps each entity to its retained value. "
            "Values can be any JSON value, including null, false, and empty collections. "
            "An empty input returns an empty object. Do not modify the input. Calls are independent.",
    "constraints": ["0–300 events. All required fields are present.",
                    "Entity names are nonempty ASCII strings of at most 80 characters.",
                    "Versions are integers from 1 to 1000000000. Inputs satisfy the contract; no validation is required."],
    "function": "latest_events",
    "starter": "def latest_events(events):\n    raise NotImplementedError\n",
    "reference": '''def latest_events(events):
    latest = {}
    for event in events:
        entity = event["entity"]
        current = latest.get(entity)
        if current is None or event["version"] > current[0]:
            latest[entity] = (event["version"], event["value"])
    return {entity: item[1] for entity, item in latest.items()}
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Long> versions = new HashMap<>();
    Map<String,Object> values = new LinkedHashMap<>();
    for (Object raw : arr(d.get("events"))) {
        Map<String,Object> event = obj(raw);
        String entity = s(event.get("entity"));
        long version = lng(event.get("version"));
        if (!versions.containsKey(entity) || version > versions.get(entity)) {
            versions.put(entity, version);
            values.put(entity, event.get("value"));
        }
    }
    return values;
}''',
    "cases": CASES,
    "mutations": [
        {"name": "equal_version_overwrites_first", "old": 'event["version"] > current[0]',
         "new": 'event["version"] >= current[0]'},
        {"name": "stale_event_overwrites_latest", "old": 'current is None or event["version"] > current[0]',
         "new": 'True'},
        {"name": "returns_version_instead_of_value", "old": 'entity: item[1]',
         "new": 'entity: item[0]'},
    ],
}

# Bound decimal precision so Python and the independent marker preserve the same JSON value.
SPEC["constraints"].append("Floating-point values have at most six decimal places and an absolute value at most 1000000.")
SPEC["cases"].append({'input': {'events': [{'entity': 'x', 'version': 1, 'value': [1e-06, -999999.999999]}]}, 'expected': {'x': [1e-06, -999999.999999]}, 'label': 'decimal value boundaries'})
