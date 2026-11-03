## How it works

A dictionary maps each key to its first task and ID. A new key creates a job. A known key returns the saved ID when the task matches, or a conflict when it does not.

## Common mistakes

- Giving an ID to replays or conflicts, so the IDs have gaps.
- Returning a new ID for a replay instead of the original ID.
- Accepting a changed task as a replay.

## Solution

```python
def enqueue_jobs(requests):
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
```
