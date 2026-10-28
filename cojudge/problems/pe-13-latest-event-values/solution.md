## Reference solution

```python
def latest_events(events):
    latest = {}
    for event in events:
        entity = event["entity"]
        current = latest.get(entity)
        if current is None or event["version"] > current[0]:
            latest[entity] = (event["version"], event["value"])
    return {entity: item[1] for entity, item in latest.items()}
```
