A consumer must ignore stale events and retain the latest value for each entity.

Implement `latest_events(events)`. Each event has `entity`, `version`, and `value`. Return a dictionary that maps each entity to its latest value.

Process events in order. Store the first event for each entity. Replace its value only for a strictly greater version. The first event wins a version tie.

Keep any JSON value, including `None`, `False`, and empty collections. Empty input returns an empty dictionary.

**Constraints:**

- 0–300 events. All required fields are present.
- Entity names are nonempty ASCII strings of at most 80 characters.
- Versions are integers from 1 to 1000000000.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change input objects or their nested values. Each call starts with fresh state.
