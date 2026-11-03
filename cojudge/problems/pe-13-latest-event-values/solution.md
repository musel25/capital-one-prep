## How it works

Save the version and the value for each entity. A new event wins only with a higher version. So late and repeated events do not overwrite newer data.

## Common mistakes

- Letting an equal version overwrite the first event.
- Letting a stale event overwrite a newer one.
- Returning the version instead of the value.

## Solution

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
