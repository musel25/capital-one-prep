**The ticket.** A consumer reads update events from a queue. Events can arrive late or out of order. Each event has a version number.

**Why it matters.** If you keep the last event that arrives, a late old event overwrites new data. The version number tells you which data is newer.

### Your task

Write `latest_events(events)`. Each event has `entity`, `version`, and `value`. Return a dictionary from each entity to its latest value.

1. Process the events in order.
2. Save the first event for each entity.
3. Replace the saved value only when the new version is strictly greater. On an equal or smaller version, ignore the event.
4. Return the values, not the versions. A value can be any JSON value, also `None` or `False`.

**Constraints:**

- 0–300 events. Entity names are nonempty strings. Versions are integers from 1 to 1000000000.
