## Reference solution

```python
def process_queue(operations, visibility):
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
```
