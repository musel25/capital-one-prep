## Reference solution

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
