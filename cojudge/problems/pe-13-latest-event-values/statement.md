A consumer must ignore stale events and retain the latest value for each entity.

Implement `latest_events(events)`. Each event has `entity`, `version`, and `value`. Process events in input order. Store the first event for each entity. Replace its value only when a later event has a strictly greater version. The first event wins when versions are equal. Return an object that maps each entity to its retained value. Values can be any JSON value, including null, false, and empty collections. An empty input returns an empty object. Do not modify the input. Calls are independent.

**Constraints:**

- 0–300 events. All required fields are present.
- Entity names are nonempty ASCII strings of at most 80 characters.
- Versions are integers from 1 to 1000000000. Inputs satisfy the contract; no validation is required.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `latest_events`. **Run** checks the examples. **Submit** checks all 15 cases.
