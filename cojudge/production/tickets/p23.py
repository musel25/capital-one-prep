"""Plan record synchronization without inferring deletions."""

CASES = [
    {"label": "plan uploads downloads and conflicts together", "input": {"local": [{"id": "local", "version": 1, "checksum": "a"}, {"id": "newer", "version": 2, "checksum": "b"}, {"id": "conflict", "version": 1, "checksum": "c"}], "remote": [{"id": "remote", "version": 1, "checksum": "d"}, {"id": "newer", "version": 1, "checksum": "b"}, {"id": "conflict", "version": 1, "checksum": "e"}]}, "expected": {"upload": ["local", "newer"], "download": ["remote"], "conflicts": ["conflict"]}},
    {"label": "higher remote version downloads", "input": {"local": [{"id": "a", "version": 1, "checksum": "old"}], "remote": [{"id": "a", "version": 2, "checksum": "new"}]}, "expected": {"upload": [], "download": ["a"], "conflicts": []}},
    {"label": "equal records need no action", "input": {"local": [{"id": "a", "version": 2, "checksum": "same"}], "remote": [{"id": "a", "version": 2, "checksum": "same"}]}, "expected": {"upload": [], "download": [], "conflicts": []}},
    {"label": "both lists empty", "input": {"local": [], "remote": []}, "expected": {"upload": [], "download": [], "conflicts": []}},
    {"label": "local-only record uploads instead of deleting", "input": {"local": [{"id": "a", "version": 0, "checksum": ""}], "remote": []}, "expected": {"upload": ["a"], "download": [], "conflicts": []}},
    {"label": "remote-only record downloads instead of deleting", "input": {"local": [], "remote": [{"id": "a", "version": 0, "checksum": ""}]}, "expected": {"upload": [], "download": ["a"], "conflicts": []}},
    {"label": "newer local version wins even with equal checksums", "input": {"local": [{"id": "a", "version": 3, "checksum": "same"}], "remote": [{"id": "a", "version": 2, "checksum": "same"}]}, "expected": {"upload": ["a"], "download": [], "conflicts": []}},
    {"label": "newer remote version wins even with equal checksums", "input": {"local": [{"id": "a", "version": 2, "checksum": "same"}], "remote": [{"id": "a", "version": 3, "checksum": "same"}]}, "expected": {"upload": [], "download": ["a"], "conflicts": []}},
    {"label": "equal zero versions with changed checksum conflict", "input": {"local": [{"id": "a", "version": 0, "checksum": "left"}], "remote": [{"id": "a", "version": 0, "checksum": "right"}]}, "expected": {"upload": [], "download": [], "conflicts": ["a"]}},
    {"label": "IDs are case sensitive", "input": {"local": [{"id": "a", "version": 1, "checksum": "x"}], "remote": [{"id": "A", "version": 1, "checksum": "x"}]}, "expected": {"upload": ["a"], "download": ["A"], "conflicts": []}},
    {"label": "all output lists use ASCII order", "input": {"local": [{"id": "z", "version": 1, "checksum": "x"}, {"id": "A", "version": 1, "checksum": "x"}, {"id": "b", "version": 1, "checksum": "x"}, {"id": "Z", "version": 1, "checksum": "x"}], "remote": [{"id": "a", "version": 1, "checksum": "x"}, {"id": "0", "version": 1, "checksum": "x"}, {"id": "b", "version": 1, "checksum": "y"}, {"id": "Z", "version": 1, "checksum": "y"}]}, "expected": {"upload": ["A", "z"], "download": ["0", "a"], "conflicts": ["Z", "b"]}},
    {"label": "checksum matching is case sensitive", "input": {"local": [{"id": "a", "version": 1, "checksum": "abc"}], "remote": [{"id": "a", "version": 1, "checksum": "ABC"}]}, "expected": {"upload": [], "download": [], "conflicts": ["a"]}},
    {"label": "empty checksums can match", "input": {"local": [{"id": "a", "version": 0, "checksum": ""}], "remote": [{"id": "a", "version": 0, "checksum": ""}]}, "expected": {"upload": [], "download": [], "conflicts": []}},
    {"label": "empty checksum differs from nonempty", "input": {"local": [{"id": "a", "version": 1, "checksum": ""}], "remote": [{"id": "a", "version": 1, "checksum": "x"}]}, "expected": {"upload": [], "download": [], "conflicts": ["a"]}},
    {"label": "maximum version wins over zero", "input": {"local": [{"id": "a", "version": 1000000000, "checksum": "x"}], "remote": [{"id": "a", "version": 0, "checksum": "y"}]}, "expected": {"upload": ["a"], "download": [], "conflicts": []}},
    {"label": "list positions do not identify records", "input": {"local": [{"id": "b", "version": 1, "checksum": "b"}, {"id": "a", "version": 3, "checksum": "a"}], "remote": [{"id": "a", "version": 2, "checksum": "a"}, {"id": "b", "version": 2, "checksum": "b"}]}, "expected": {"upload": ["a"], "download": ["b"], "conflicts": []}},
]

SPEC = {
    "number": 23,
    "slug": "reconcile-record-snapshots",
    "title": "Plan record synchronization",
    "difficulty": "Medium",
    "category": "06-application-logic",
    "ticket": "The sync client needs an action plan for local and remote records without inferring deletions.",
    "task": "Implement `reconcile_records(local, remote)`. Each list contains records with `id`, `version`, and `checksum`. IDs are unique within each list. For an ID found only locally, upload it. For an ID found only remotely, download it. For an ID on both sides, upload when its local version is higher and download when its remote version is higher. When versions are equal, matching checksums require no action; different checksums produce a conflict. Version comparison takes priority over checksum comparison. Return `{'upload': [...], 'download': [...], 'conflicts': [...]}` with IDs in ASCII lexical order within each list. Compare IDs and checksums exactly. Do not infer deletions. Do not change the input.",
    "constraints": ["Each list has 0 through 200 records with all three required fields.", "IDs are nonempty ASCII strings; checksums are ASCII strings and can be empty.", "Versions are integers from 0 through 1000000000; booleans are not versions.", "IDs are unique within each list, but can occur in both lists."],
    "function": "reconcile_records",
    "starter": "def reconcile_records(local, remote):\n    raise NotImplementedError\n",
    "reference": '''def reconcile_records(local, remote):
    local_by_id = {record["id"]: record for record in local}
    remote_by_id = {record["id"]: record for record in remote}
    result = {"upload": [], "download": [], "conflicts": []}
    for record_id in sorted(local_by_id.keys() | remote_by_id.keys()):
        if record_id not in remote_by_id:
            result["upload"].append(record_id)
        elif record_id not in local_by_id:
            result["download"].append(record_id)
        else:
            left, right = local_by_id[record_id], remote_by_id[record_id]
            if left["version"] > right["version"]:
                result["upload"].append(record_id)
            elif left["version"] < right["version"]:
                result["download"].append(record_id)
            elif left["checksum"] != right["checksum"]:
                result["conflicts"].append(record_id)
    return result
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Map<String,Object>> local = new HashMap<>(), remote = new HashMap<>();
    for (Object value : arr(d.get("local"))) {
        Map<String,Object> record = obj(value);
        local.put(s(record.get("id")), record);
    }
    for (Object value : arr(d.get("remote"))) {
        Map<String,Object> record = obj(value);
        remote.put(s(record.get("id")), record);
    }
    SortedSet<String> ids = new TreeSet<>(local.keySet());
    ids.addAll(remote.keySet());
    List<Object> upload = new ArrayList<>(), download = new ArrayList<>(), conflicts = new ArrayList<>();
    for (String id : ids) {
        Map<String,Object> left = local.get(id), right = remote.get(id);
        if (right == null) upload.add(id);
        else if (left == null) download.add(id);
        else {
            int comparison = Integer.compare(n(left.get("version")), n(right.get("version")));
            if (comparison > 0) upload.add(id);
            else if (comparison < 0) download.add(id);
            else if (!s(left.get("checksum")).equals(s(right.get("checksum")))) conflicts.add(id);
        }
    }
    return map("upload", upload, "download", download, "conflicts", conflicts);
}''',
    "cases": CASES,
    "mutations": [
        {"name": "upload equal versions", "old": 'if left["version"] > right["version"]:', "new": 'if left["version"] >= right["version"]:'},
        {"name": "conflict on matching checksums", "old": 'elif left["checksum"] != right["checksum"]:', "new": 'elif left["checksum"] == right["checksum"]:'},
        {"name": "reverse action-list ordering", "old": "sorted(local_by_id.keys() | remote_by_id.keys())", "new": "sorted(local_by_id.keys() | remote_by_id.keys(), reverse=True)"},
        {"name": "download local-only records", "old": 'if record_id not in remote_by_id:\n            result["upload"].append(record_id)', "new": 'if record_id not in remote_by_id:\n            result["download"].append(record_id)'},
    ],
}
