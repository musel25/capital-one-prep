"""Group timestamped events by their UTC calendar date."""

CASES = [
    {"input": {"timestamps": ["2026-10-28T00:30:00+02:00", "2026-10-27T23:30:00Z"]}, "expected": {"2026-10-27": 2}, "label": "positive offset moves an event to the prior UTC day"},
    {"input": {"timestamps": ["2026-10-28T23:30:00-02:00", "2026-10-29T00:00:00Z"]}, "expected": {"2026-10-29": 2}, "label": "negative offset moves an event to the next UTC day"},
    {"input": {"timestamps": []}, "expected": {}, "label": "empty timestamp list"},
    {"input": {"timestamps": ["2026-10-28T00:00:00Z", "2026-10-28T23:59:59Z"]}, "expected": {"2026-10-28": 2}, "label": "UTC day boundaries"},
    {"input": {"timestamps": ["2026-10-28T12:00:00Z", "2026-10-28T12:00:00Z"]}, "expected": {"2026-10-28": 2}, "label": "duplicate timestamps count separately"},
    {"input": {"timestamps": ["2024-03-01T00:30:00+01:00"]}, "expected": {"2024-02-29": 1}, "label": "cross into leap day"},
    {"input": {"timestamps": ["2000-02-29T23:30:00-01:00"]}, "expected": {"2000-03-01": 1}, "label": "leave leap day in a century leap year"},
    {"input": {"timestamps": ["2000-01-01T00:00:00+14:00"]}, "expected": {"1999-12-31": 1}, "label": "UTC output may precede the input year range"},
    {"input": {"timestamps": ["2099-12-31T23:59:59-14:00"]}, "expected": {"2100-01-01": 1}, "label": "UTC output may follow the input year range"},
    {"input": {"timestamps": ["2026-01-01T00:15:00+00:30"]}, "expected": {"2025-12-31": 1}, "label": "positive offset with nonzero minutes"},
    {"input": {"timestamps": ["2026-04-30T23:30:00-00:45"]}, "expected": {"2026-05-01": 1}, "label": "negative offset with nonzero minutes"},
    {"input": {"timestamps": ["2026-10-29T00:00:00Z", "2026-10-27T00:00:00Z", "2026-10-28T00:00:00Z", "2026-10-27T23:59:59Z"]}, "expected": {"2026-10-27": 2, "2026-10-28": 1, "2026-10-29": 1}, "label": "unsorted timestamps form separate date groups"},
    {"input": {"timestamps": ["2026-10-28T00:00:00+00:00", "2026-10-28T00:00:00-00:00", "2026-10-28T00:00:00Z"]}, "expected": {"2026-10-28": 3}, "label": "all zero-offset forms are equivalent"},
    {"input": {"timestamps": ["2026-10-28T13:59:59+14:00", "2026-10-28T14:00:00+14:00"]}, "expected": {"2026-10-27": 1, "2026-10-28": 1}, "label": "one second across midnight at the maximum offset"},
]

SPEC = {
    "number": 18,
    "slug": "utc-day-counts",
    "title": "Count events by UTC day",
    "difficulty": "Medium",
    "category": "05-files-time-and-boundaries",
    "ticket": "The daily event report must group offset timestamps by UTC date instead of their displayed local date.",
    "task": "Implement count_utc_days(timestamps). Each string is a valid timestamp in exactly one form: YYYY-MM-DDTHH:MM:SSZ, YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM. Convert each timestamp to UTC before taking its calendar date. Return an object mapping each UTC date, formatted YYYY-MM-DD, to its occurrence count. Count duplicate timestamps separately. Input order does not matter, and object key order does not matter. An empty list returns an empty object. UTC conversion may move a date into 1999 or 2100 even though input years are 2000–2099. Do not change the input list. Invalid dates, missing offsets, fractional seconds and other timestamp forms are outside the contract; no validation is required for them.",
    "constraints": ["0–200 timestamps; input years are 2000 through 2099 with valid calendar dates.", "Hours are 00–23, minutes and seconds are 00–59; leap seconds are excluded.", "Offsets have absolute value at most 14:00; offset minutes are 00–59, and hour 14 requires minute 00.", "No local timezone or clock access is required. Each call is independent."],
    "function": "count_utc_days",
    "starter": "def count_utc_days(timestamps):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''from datetime import datetime, timezone


def count_utc_days(timestamps):
    counts = {}
    for timestamp in timestamps:
        parsed = datetime.fromisoformat(timestamp)
        day = parsed.astimezone(timezone.utc).date().isoformat()
        counts[day] = counts.get(day, 0) + 1
    return counts
'''

SPEC["java"] = '''public Object solve(Map<String,Object> d) {
    Map<String,Object> counts = new LinkedHashMap<>();
    for (Object timestamp : arr(d.get("timestamps"))) {
        OffsetDateTime parsed = OffsetDateTime.parse(s(timestamp));
        String day = parsed.withOffsetSameInstant(ZoneOffset.UTC).toLocalDate().toString();
        counts.put(day, counts.containsKey(day) ? n(counts.get(day)) + 1 : 1);
    }
    return counts;
}
'''

SPEC["mutations"] = [
    {"name": "group by local date", "old": 'parsed.astimezone(timezone.utc).date().isoformat()', "new": 'parsed.date().isoformat()'},
    {"name": "overwrite repeated day counts", "old": 'counts.get(day, 0) + 1', "new": '1'},
    {"name": "replace offsets instead of converting them", "old": 'datetime.fromisoformat(timestamp)', "new": 'datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)'},
    {"name": "format only the month and day", "old": '.date().isoformat()', "new": '.date().strftime("%m-%d")'},
]
