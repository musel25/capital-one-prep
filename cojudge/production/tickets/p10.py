"""Allocate job IDs with exact idempotency-key replay rules."""

CASES = [
    {"label": "new keys get consecutive IDs", "input": {"requests": [{"key": "a", "task": "send"}, {"key": "b", "task": "index"}]}, "expected": [{"status": "created", "id": 1}, {"status": "created", "id": 2}]},
    {"label": "same key and task replays original ID", "input": {"requests": [{"key": "a", "task": "send"}, {"key": "a", "task": "send"}]}, "expected": [{"status": "created", "id": 1}, {"status": "replayed", "id": 1}]},
    {"label": "changed task conflicts without replacing original", "input": {"requests": [{"key": "a", "task": "old"}, {"key": "a", "task": "new"}, {"key": "a", "task": "old"}]}, "expected": [{"status": "created", "id": 1}, {"status": "conflict", "id": None}, {"status": "replayed", "id": 1}]},
    {"label": "empty batch", "input": {"requests": []}, "expected": []},
    {"label": "identical tasks with different keys are new jobs", "input": {"requests": [{"key": "a", "task": "same"}, {"key": "b", "task": "same"}]}, "expected": [{"status": "created", "id": 1}, {"status": "created", "id": 2}]},
    {"label": "empty task can be replayed", "input": {"requests": [{"key": "empty", "task": ""}, {"key": "empty", "task": ""}]}, "expected": [{"status": "created", "id": 1}, {"status": "replayed", "id": 1}]},
    {"label": "key matching is case sensitive", "input": {"requests": [{"key": "a", "task": "x"}, {"key": "A", "task": "x"}]}, "expected": [{"status": "created", "id": 1}, {"status": "created", "id": 2}]},
    {"label": "task matching is case sensitive", "input": {"requests": [{"key": "a", "task": "x"}, {"key": "a", "task": "X"}]}, "expected": [{"status": "created", "id": 1}, {"status": "conflict", "id": None}]},
    {"label": "conflict does not consume an ID", "input": {"requests": [{"key": "a", "task": "x"}, {"key": "a", "task": "y"}, {"key": "b", "task": "y"}]}, "expected": [{"status": "created", "id": 1}, {"status": "conflict", "id": None}, {"status": "created", "id": 2}]},
    {"label": "replay does not consume an ID", "input": {"requests": [{"key": "a", "task": "x"}, {"key": "a", "task": "x"}, {"key": "b", "task": "x"}]}, "expected": [{"status": "created", "id": 1}, {"status": "replayed", "id": 1}, {"status": "created", "id": 2}]},
    {"label": "repeated conflicting task remains a conflict", "input": {"requests": [{"key": "a", "task": "x"}, {"key": "a", "task": "y"}, {"key": "a", "task": "y"}]}, "expected": [{"status": "created", "id": 1}, {"status": "conflict", "id": None}, {"status": "conflict", "id": None}]},
    {"label": "keys and tasks are not stripped", "input": {"requests": [{"key": " a ", "task": " x "}, {"key": "a", "task": " x "}, {"key": " a ", "task": "x"}]}, "expected": [{"status": "created", "id": 1}, {"status": "created", "id": 2}, {"status": "conflict", "id": None}]},
    {"label": "interleaved replay returns each original ID", "input": {"requests": [{"key": "a", "task": "x"}, {"key": "b", "task": "y"}, {"key": "a", "task": "x"}, {"key": "b", "task": "y"}]}, "expected": [{"status": "created", "id": 1}, {"status": "created", "id": 2}, {"status": "replayed", "id": 1}, {"status": "replayed", "id": 2}]},
    {"label": "ASCII control characters remain exact data", "input": {"requests": [{"key": "\t", "task": "line\n"}, {"key": "\t", "task": "line\n"}, {"key": "\t", "task": "line"}]}, "expected": [{"status": "created", "id": 1}, {"status": "replayed", "id": 1}, {"status": "conflict", "id": None}]},
]

SPEC = {
    "number": 10,
    "slug": "enqueue-idempotent-jobs",
    "title": "Handle duplicate job submissions",
    "difficulty": "Medium",
    "category": "02-clients-and-reliability",
    "ticket": "The job queue must replay duplicate submissions and reject reuse of a key for a different task.",
    "task": "Implement `enqueue_jobs(requests)`. Each request has a nonempty ASCII string `key` and an ASCII string `task`, which can be empty. Process requests in order. For a new key, store its task, allocate the next integer ID starting at 1, and return `{'status': 'created', 'id': ID}`. For an existing key with the same task, return `{'status': 'replayed', 'id': ORIGINAL_ID}`. For an existing key with a different task, return `{'status': 'conflict', 'id': null}`. A replay or conflict consumes no ID. A conflict changes no stored key, task, or ID. Compare strings exactly. Return one response per request in input order. Empty input returns an empty list. Each function call starts with an empty queue and ID 1. Do not change the input.",
    "constraints": ["All requests contain key and task with the stated string types.", "Keys are nonempty ASCII strings; tasks can be empty.", "Only a newly accepted key allocates an ID."],
    "function": "enqueue_jobs",
    "starter": "def enqueue_jobs(requests):\n    raise NotImplementedError\n",
    "reference": '''def enqueue_jobs(requests):
    jobs = {}
    next_id = 1
    responses = []
    for request in requests:
        key, task = request["key"], request["task"]
        if key not in jobs:
            jobs[key] = (task, next_id)
            responses.append({"status": "created", "id": next_id})
            next_id += 1
        elif task == jobs[key][0]:
            responses.append({"status": "replayed", "id": jobs[key][1]})
        else:
            responses.append({"status": "conflict", "id": None})
    return responses
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Map<String,Object>> jobs = new HashMap<>();
    List<Object> responses = new ArrayList<>();
    int nextId = 1;
    for (Object raw : arr(d.get("requests"))) {
        Map<String,Object> request = obj(raw);
        String key = s(request.get("key"));
        String task = s(request.get("task"));
        Map<String,Object> saved = jobs.get(key);
        if (saved == null) {
            jobs.put(key, map("task", task, "id", nextId));
            responses.add(map("status", "created", "id", nextId));
            nextId++;
        } else if (task.equals(s(saved.get("task")))) {
            responses.add(map("status", "replayed", "id", saved.get("id")));
        } else {
            responses.add(map("status", "conflict", "id", null));
        }
    }
    return responses;
}''',
    "cases": CASES,
    "mutations": [
        {"name": "allocate IDs with gaps", "old": "next_id += 1", "new": "next_id += 2"},
        {"name": "replay the next ID instead of original", "old": 'responses.append({"status": "replayed", "id": jobs[key][1]})', "new": 'responses.append({"status": "replayed", "id": next_id})'},
        {"name": "accept a changed task as a replay", "old": "elif task == jobs[key][0]:", "new": "elif True:"},
        {"name": "strip task whitespace before comparing", "old": "elif task == jobs[key][0]:", "new": "elif task.strip() == jobs[key][0].strip():"},
    ],
}
