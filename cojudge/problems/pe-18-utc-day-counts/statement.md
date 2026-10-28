# 18. Count events by UTC day

The daily event report must group offset timestamps by UTC date instead of their displayed local date.

Implement count_utc_days(timestamps). Each string is a valid timestamp in exactly one form: YYYY-MM-DDTHH:MM:SSZ, YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM. Convert each timestamp to UTC before taking its calendar date. Return an object mapping each UTC date, formatted YYYY-MM-DD, to its occurrence count. Count duplicate timestamps separately. Input order does not matter, and object key order does not matter. An empty list returns an empty object. UTC conversion may move a date into 1999 or 2100 even though input years are 2000–2099. Do not change the input list. Invalid dates, missing offsets, fractional seconds and other timestamp forms are outside the contract; no validation is required for them.

**Constraints:**

- 0–200 timestamps; input years are 2000 through 2099 with valid calendar dates.
- Hours are 00–23, minutes and seconds are 00–59; leap seconds are excluded.
- Offsets have absolute value at most 14:00; offset minutes are 00–59, and hour 14 requires minute 00.
- No local timezone or clock access is required. Each call is independent.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `count_utc_days`. **Run** checks the examples. **Submit** checks all 14 cases.
