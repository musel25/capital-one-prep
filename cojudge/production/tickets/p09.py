"""Follow API page tokens without losing partial results."""

CASES = [
    {"label": "deduplicate across pages in arrival order", "input": {"pages": {"a": {"items": [3, 1, 3], "next": "b"}, "b": {"items": [1, 2, 0], "next": None}}, "start": "a"}, "expected": {"items": [3, 1, 2, 0], "error": None}},
    {"label": "keep items before missing next page", "input": {"pages": {"a": {"items": [7], "next": "absent"}}, "start": "a"}, "expected": {"items": [7], "error": "missing_page"}},
    {"label": "stop before reading a repeated page", "input": {"pages": {"a": {"items": [2], "next": "b"}, "b": {"items": [4, 2], "next": "a"}}, "start": "a"}, "expected": {"items": [2, 4], "error": "cycle"}},
    {"label": "null start with no pages", "input": {"pages": {}, "start": None}, "expected": {"items": [], "error": None}},
    {"label": "null start ignores available pages", "input": {"pages": {"a": {"items": [1], "next": "a"}}, "start": None}, "expected": {"items": [], "error": None}},
    {"label": "missing initial page", "input": {"pages": {}, "start": "a"}, "expected": {"items": [], "error": "missing_page"}},
    {"label": "empty terminal page", "input": {"pages": {"a": {"items": [], "next": None}}, "start": "a"}, "expected": {"items": [], "error": None}},
    {"label": "empty page does not terminate traversal", "input": {"pages": {"a": {"items": [], "next": "b"}, "b": {"items": [8], "next": None}}, "start": "a"}, "expected": {"items": [8], "error": None}},
    {"label": "self cycle", "input": {"pages": {"a": {"items": [6, 6], "next": "a"}}, "start": "a"}, "expected": {"items": [6], "error": "cycle"}},
    {"label": "ignore unreachable broken chain", "input": {"pages": {"a": {"items": [9], "next": None}, "broken": {"items": [1], "next": "gone"}}, "start": "a"}, "expected": {"items": [9], "error": None}},
    {"label": "page tokens are case sensitive", "input": {"pages": {"A": {"items": [5], "next": "a"}, "a": {"items": [1], "next": None}}, "start": "A"}, "expected": {"items": [5, 1], "error": None}},
    {"label": "zero is a real item ID", "input": {"pages": {"zero": {"items": [0, 0, 2, 0], "next": None}}, "start": "zero"}, "expected": {"items": [0, 2], "error": None}},
    {"label": "integer IDs do not truncate", "input": {"pages": {"a": {"items": [18446744073709551616, 0, 18446744073709551616], "next": None}}, "start": "a"}, "expected": {"items": [18446744073709551616, 0], "error": None}},
    {"label": "missing page after empty result", "input": {"pages": {"a": {"items": [], "next": "gone"}}, "start": "a"}, "expected": {"items": [], "error": "missing_page"}},
    {"label": "cycle starts after an acyclic prefix", "input": {"pages": {"a": {"items": [8], "next": "b"}, "b": {"items": [], "next": "c"}, "c": {"items": [8, 3], "next": "b"}}, "start": "a"}, "expected": {"items": [8, 3], "error": "cycle"}},
    {"label": "tokens are not stripped", "input": {"pages": {" a ": {"items": [4], "next": "a"}, "a": {"items": [2], "next": None}}, "start": " a "}, "expected": {"items": [4, 2], "error": None}},
]

SPEC = {
    "number": 9,
    "slug": "collect-api-pages",
    "title": "Keep partial results from paginated APIs",
    "difficulty": "Medium",
    "category": "02-clients-and-reliability",
    "ticket": "Our API client must stop on broken page chains and retain the IDs it already received.",
    "task": "Implement `collect_pages(pages, start)`. `pages` maps nonempty ASCII tokens to objects with an `items` list of nonnegative integer IDs and a `next` token or null. `start` is a token or null. Follow `next` until null. Return `{'items': [...], 'error': null}` on success. Keep each ID once, in first-seen order. If a token is absent from `pages`, stop before reading it and return error `'missing_page'`. If a token was already visited, stop before reading it again and return error `'cycle'`. Keep all IDs collected before either error. A null start returns empty items and a null error. Ignore pages outside the followed chain. Compare tokens exactly. Do not change the input.",
    "constraints": ["All page records contain items and next with the stated types.", "Tokens are nonempty ASCII strings; null is the only end marker.", "IDs are integers greater than or equal to zero; booleans are not IDs."],
    "function": "collect_pages",
    "starter": "def collect_pages(pages, start):\n    raise NotImplementedError\n",
    "reference": '''def collect_pages(pages, start):
    items = []
    seen_ids = set()
    visited = set()
    token = start
    while token is not None:
        if token in visited:
            return {"items": items, "error": "cycle"}
        if token not in pages:
            return {"items": items, "error": "missing_page"}
        visited.add(token)
        page = pages[token]
        for item in page["items"]:
            if item not in seen_ids:
                seen_ids.add(item)
                items.append(item)
        token = page["next"]
    return {"items": items, "error": None}
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Object> pages = obj(d.get("pages"));
    String token = d.get("start") == null ? null : s(d.get("start"));
    Set<String> visited = new HashSet<>();
    Set<Object> seenIds = new HashSet<>();
    List<Object> items = new ArrayList<>();
    while (token != null) {
        if (visited.contains(token)) return map("items", items, "error", "cycle");
        if (!pages.containsKey(token)) return map("items", items, "error", "missing_page");
        visited.add(token);
        Map<String,Object> page = obj(pages.get(token));
        for (Object item : arr(page.get("items"))) {
            if (seenIds.add(item)) items.add(item);
        }
        token = page.get("next") == null ? null : s(page.get("next"));
    }
    return map("items", items, "error", null);
}''',
    "cases": CASES,
    "mutations": [
        {"name": "keep duplicate IDs", "old": "if item not in seen_ids:", "new": "if True:"},
        {"name": "discard partial results on a missing page", "old": 'return {"items": items, "error": "missing_page"}', "new": 'return {"items": [], "error": "missing_page"}'},
        {"name": "report cycle as success", "old": 'return {"items": items, "error": "cycle"}', "new": 'return {"items": items, "error": None}'},
        {"name": "drop zero IDs", "old": "if item not in seen_ids:", "new": "if item and item not in seen_ids:"},
    ],
}
