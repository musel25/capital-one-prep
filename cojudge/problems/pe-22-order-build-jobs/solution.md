## Reference solution

```python
def build_order(dependencies):
    remaining = {job: set(prerequisites) for job, prerequisites in dependencies.items()}
    ordered = []
    while remaining:
        ready = sorted(job for job, needed in remaining.items() if not needed)
        if not ready:
            return None
        job = ready[0]
        ordered.append(job)
        del remaining[job]
        for needed in remaining.values():
            needed.discard(job)
    return ordered
```
