"""Deliver queue jobs with visibility deadlines."""


def enqueue(job, at=0):
    return {"op": "enqueue", "id": job, "at": at}


def poll(at=0):
    return {"op": "poll", "at": at}


def ack(job, at=0):
    return {"op": "ack", "id": job, "at": at}


def case(operations, expected, label, visibility=5):
    return {"input": {"operations": operations, "visibility": visibility},
            "expected": expected, "label": label}


CASES = [
    case([], [], "empty operation list"),
    case([poll(), ack("missing")], [None, False], "empty queue and unknown acknowledgment"),
    case([enqueue("a"), poll(), ack("a", 4), poll(4)],
         [None, "a", True, None], "acknowledged job is removed"),
    case([enqueue("a"), poll(), poll(4)], [None, "a", None], "invisible before exact expiry"),
    case([enqueue("a"), poll(), ack("a", 5), poll(5)],
         [None, "a", False, "a"], "ack fails and redelivery succeeds at exact expiry"),
    case([enqueue("a"), ack("a"), poll()], [None, False, "a"], "unpolled job cannot be acknowledged"),
    case([enqueue("a"), enqueue("b"), poll(), poll(), poll()],
         [None, None, "a", "b", None], "FIFO skips in-flight jobs"),
    case([enqueue("a"), enqueue("b"), poll(), poll(5), poll(5)],
         [None, None, "a", "a", "b"], "expired earlier job precedes never-polled job"),
    case([enqueue("a"), poll(), ack("a", 1), ack("a", 1)],
         [None, "a", True, False], "duplicate acknowledgment fails"),
    case([enqueue("a"), poll(), ack("other", 1), ack("a", 1)],
         [None, "a", False, True], "unknown acknowledgment preserves in-flight job"),
    case([enqueue("a"), poll(), ack("a", 6), poll(6), ack("a", 10)],
         [None, "a", False, "a", True], "redelivery starts a new visibility deadline"),
    case([enqueue("a"), poll(), poll(5), poll(9), poll(10)],
         [None, "a", "a", None, "a"], "deadline extends from redelivery time"),
    case([enqueue("a"), poll(), ack("a"), poll(), enqueue("b"), poll()],
         [None, "a", True, None, None, "b"], "same-time operations follow input order"),
    case([enqueue("a"), poll(), poll(1), ack("a", 1)],
         [None, "a", "a", True], "minimum visibility and same-time redelivery acknowledgment", 1),
    case([enqueue("a", 1000000000), poll(1000000000), poll(1000000999), poll(1000001000)],
         [None, "a", None, "a"], "maximum visibility with large clock values", 1000),
    case([enqueue("a"), enqueue("b"), enqueue("c"), poll(), poll(1), ack("b", 2), poll(5), poll(5)],
         [None, None, None, "a", "b", True, "a", "c"], "acknowledgment does not reorder other jobs"),
]

CASES = CASES[2:5] + CASES[:2] + CASES[5:]

SPEC = {
    "number": 15,
    "slug": "queue-visibility",
    "title": "Deliver jobs with a visibility timeout",
    "difficulty": "Hard",
    "category": "04-jobs-and-storage",
    "ticket": "A worker queue must redeliver unacknowledged jobs after their visibility timeout.",
    "task": "Implement `process_queue(operations, visibility)`. Process operations in input order. "
            "`enqueue` has `id` and `at`: append a job and return null. `poll` has `at`: return the "
            "earliest unacknowledged job in enqueue order that has never been polled or whose "
            "deadline is at or before `at`; return null if none exists. A successful poll sets its "
            "deadline to `at + visibility`. `ack` has `id` and `at`: remove the job and return true "
            "only if it is currently in flight and `at` is strictly before its deadline. Otherwise, "
            "return false without a state change. At exact expiry, acknowledgment fails and polling "
            "can redeliver the job. Return a list with one result per operation. An empty list "
            "returns an empty list. Do not modify the input. Calls are independent.",
    "constraints": ["0–300 operations. All required fields are present; op is enqueue, poll, or ack.",
                    "Job IDs are nonempty ASCII strings of at most 80 characters. Each ID is enqueued at most once.",
                    "Times are integers from 0 to 2000000000 in nondecreasing order. Equal times are allowed.",
                    "Visibility is an integer from 1 to 1000. Operations run sequentially; no parallel execution.",
                    "Inputs satisfy the contract; no validation is required."],
    "function": "process_queue",
    "starter": "def process_queue(operations, visibility):\n    raise NotImplementedError\n",
    "reference": '''def process_queue(operations, visibility):
    jobs = []
    outputs = []
    for operation in operations:
        now = operation["at"]
        kind = operation["op"]
        if kind == "enqueue":
            jobs.append({"id": operation["id"], "deadline": None})
            outputs.append(None)
        elif kind == "poll":
            result = None
            for job in jobs:
                if job["deadline"] is None or job["deadline"] <= now:
                    job["deadline"] = now + visibility
                    result = job["id"]
                    break
            outputs.append(result)
        else:
            job = next((job for job in jobs if job["id"] == operation["id"]), None)
            ok = job is not None and job["deadline"] is not None and now < job["deadline"]
            if ok:
                jobs.remove(job)
            outputs.append(ok)
    return outputs
''',
    "java": '''public Object solve(Map<String,Object> d) {
    long visibility = lng(d.get("visibility"));
    LinkedHashMap<String,Long> deadlines = new LinkedHashMap<>();
    List<Object> outputs = new ArrayList<>();
    for (Object raw : arr(d.get("operations"))) {
        Map<String,Object> operation = obj(raw);
        long now = lng(operation.get("at"));
        String kind = s(operation.get("op"));
        if (kind.equals("enqueue")) {
            deadlines.put(s(operation.get("id")), null);
            outputs.add(null);
        } else if (kind.equals("poll")) {
            String selected = null;
            for (Map.Entry<String,Long> job : deadlines.entrySet()) {
                if (job.getValue() == null || job.getValue() <= now) {
                    selected = job.getKey();
                    job.setValue(now + visibility);
                    break;
                }
            }
            outputs.add(selected);
        } else {
            String id = s(operation.get("id"));
            Long deadline = deadlines.get(id);
            boolean ok = deadline != null && now < deadline;
            if (ok) deadlines.remove(id);
            outputs.add(ok);
        }
    }
    return outputs;
}''',
    "cases": CASES,
    "mutations": [
        {"name": "not_visible_at_exact_expiry", "old": 'job["deadline"] <= now',
         "new": 'job["deadline"] < now'},
        {"name": "ack_accepted_at_exact_expiry", "old": 'now < job["deadline"]',
         "new": 'now <= job["deadline"]'},
        {"name": "poll_uses_lifo_order", "old": 'for job in jobs:',
         "new": 'for job in reversed(jobs):'},
        {"name": "deadline_does_not_use_current_time", "old": 'job["deadline"] = now + visibility',
         "new": 'job["deadline"] = visibility'},
    ],
}
