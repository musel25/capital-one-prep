"""Return a stable page from an unsorted record collection."""

CASES = [
    {"input": {"records": [{"id": 3}, {"id": 1}, {"id": 2}], "after_id": None, "limit": 2}, "expected": {"items": [{"id": 1}, {"id": 2}], "next_cursor": 2}, "label": "sort before selecting the first page"},
    {"input": {"records": [{"id": 3}, {"id": 1}, {"id": 2}], "after_id": 1, "limit": 2}, "expected": {"items": [{"id": 2}, {"id": 3}], "next_cursor": None}, "label": "cursor is exclusive and final full page has no cursor"},
    {"input": {"records": [], "after_id": None, "limit": 1}, "expected": {"items": [], "next_cursor": None}, "label": "empty collection"},
    {"input": {"records": [], "after_id": 20, "limit": 50}, "expected": {"items": [], "next_cursor": None}, "label": "empty collection with a cursor"},
    {"input": {"records": [{"id": 1}], "after_id": 0, "limit": 1}, "expected": {"items": [{"id": 1}], "next_cursor": None}, "label": "zero cursor precedes positive IDs"},
    {"input": {"records": [{"id": 1}], "after_id": 1, "limit": 1}, "expected": {"items": [], "next_cursor": None}, "label": "cursor equals final record"},
    {"input": {"records": [{"id": 1}, {"id": 4}], "after_id": 9, "limit": 1}, "expected": {"items": [], "next_cursor": None}, "label": "cursor exceeds every ID"},
    {"input": {"records": [{"id": 9}, {"id": 2}, {"id": 5}], "after_id": 3, "limit": 1}, "expected": {"items": [{"id": 5}], "next_cursor": 5}, "label": "cursor need not match a record"},
    {"input": {"records": [{"id": 10}, {"id": 2}], "after_id": None, "limit": 1}, "expected": {"items": [{"id": 2}], "next_cursor": 2}, "label": "numeric ID order"},
    {"input": {"records": [{"id": 8, "name": "A", "active": False, "meta": {"tags": [None, "x"]}}], "after_id": None, "limit": 50}, "expected": {"items": [{"id": 8, "name": "A", "active": False, "meta": {"tags": [None, "x"]}}], "next_cursor": None}, "label": "retain all record fields"},
    {"input": {"records": [{"id": 4}, {"id": 2}], "after_id": None, "limit": 50}, "expected": {"items": [{"id": 2}, {"id": 4}], "next_cursor": None}, "label": "maximum page limit"},
    {"input": {"records": [{"id": 5}, {"id": 1}, {"id": 9}, {"id": 3}], "after_id": 3, "limit": 1}, "expected": {"items": [{"id": 5}], "next_cursor": 5}, "label": "filter before limiting"},
    {"input": {"records": [{"id": 7}, {"id": 6}, {"id": 2}], "after_id": 2, "limit": 3}, "expected": {"items": [{"id": 6}, {"id": 7}], "next_cursor": None}, "label": "short final page"},
    {"input": {"records": [{"id": 100000000000000000000}, {"id": 99999999999999999999}], "after_id": 99999999999999999999, "limit": 1}, "expected": {"items": [{"id": 100000000000000000000}], "next_cursor": None}, "label": "large integer IDs remain exact"},
]

SPEC = {
    "number": 5,
    "slug": "record-cursor-pagination",
    "title": "Return the next record page",
    "difficulty": "Easy",
    "category": "01-data-and-api",
    "ticket": "The records endpoint must return stable pages when its source records arrive out of order.",
    "task": "Implement paginate_records(records, after_id, limit). records is an unsorted list of JSON objects with unique positive integer id fields. Other fields can contain any JSON value. after_id is null or a non-negative integer; it need not match a record. Sort records by numeric id in ascending order. If after_id is not null, keep only IDs strictly greater than it. Return {'items': [...], 'next_cursor': ...}, with at most limit eligible records. next_cursor is the last returned ID only when more eligible records remain. Otherwise it is null, including for empty results and exactly full final pages. Retain every field of each selected record. Do not change the input list or records. Each call is independent.",
    "constraints": ["0–200 records; limit is an integer from 1 through 50.", "IDs are unique positive integers; after_id is null or a non-negative integer.", "Inputs satisfy the contract. No input validation, storage or network access is required."],
    "function": "paginate_records",
    "starter": "def paginate_records(records, after_id, limit):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''def paginate_records(records, after_id, limit):
    eligible = [row for row in records if after_id is None or row["id"] > after_id]
    eligible.sort(key=lambda row: row["id"])
    items = eligible[:limit]
    next_cursor = items[-1]["id"] if len(eligible) > len(items) else None
    return {"items": items, "next_cursor": next_cursor}
'''

SPEC["java"] = '''public Object solve(Map<String,Object> d) {
    List<Object> eligible = new ArrayList<>();
    Object cursor = d.get("after_id");
    BigInteger after = cursor == null ? null : new BigInteger(cursor.toString());
    for (Object row : arr(d.get("records"))) {
        BigInteger id = new BigInteger(obj(row).get("id").toString());
        if (after == null || id.compareTo(after) > 0) eligible.add(row);
    }
    eligible.sort((a, b) -> new BigInteger(obj(a).get("id").toString())
        .compareTo(new BigInteger(obj(b).get("id").toString())));
    int count = Math.min(n(d.get("limit")), eligible.size());
    List<Object> items = new ArrayList<>(eligible.subList(0, count));
    Object next = count < eligible.size() ? obj(items.get(count - 1)).get("id") : null;
    return map("items", items, "next_cursor", next);
}
'''

SPEC["mutations"] = [
    {"name": "include the cursor row", "old": 'row["id"] > after_id', "new": 'row["id"] >= after_id'},
    {"name": "preserve source order instead of sorting", "old": 'eligible.sort(key=lambda row: row["id"])', "new": 'pass'},
    {"name": "sort IDs as text", "old": 'key=lambda row: row["id"]', "new": 'key=lambda row: str(row["id"])'},
    {"name": "emit cursor on a full final page", "old": 'len(eligible) > len(items)', "new": 'bool(items) and len(eligible) >= len(items)'},
    {"name": "return one fewer record", "old": 'items = eligible[:limit]', "new": 'items = eligible[:max(0, limit - 1)]'},
]

# Bound decimal precision so Python and the independent marker preserve the same JSON value.
SPEC["constraints"].append("Floating-point values have at most six decimal places and an absolute value at most 1000000.")
SPEC["cases"].append({'input': {'records': [{'id': 1, 'amount': 999999.999999, 'tiny': 1e-06}], 'after_id': None, 'limit': 1}, 'expected': {'items': [{'id': 1, 'amount': 999999.999999, 'tiny': 1e-06}], 'next_cursor': None}, 'label': 'decimal value boundaries'})
