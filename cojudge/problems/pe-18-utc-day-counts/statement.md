The daily event report must group offset timestamps by UTC date instead of their displayed local date.

Implement `count_utc_days(timestamps)`. Convert each timestamp to UTC before taking its calendar date. Return a dictionary from `YYYY-MM-DD` dates to counts.

Count duplicate timestamps separately. Input order and dictionary key order do not matter. Empty input returns an empty dictionary. UTC conversion may produce dates in 1999 or 2100.

**Constraints:**

- 0–200 timestamps; input years are 2000 through 2099 with valid calendar dates.
- Hours are 00–23, minutes and seconds are 00–59; leap seconds are excluded.
- Offsets have absolute value at most 14:00; offset minutes are 00–59, and hour 14 requires minute 00.
- Timestamps use exactly `YYYY-MM-DDTHH:MM:SSZ`, `YYYY-MM-DDTHH:MM:SS+HH:MM`, or `YYYY-MM-DDTHH:MM:SS-HH:MM`. Fractional seconds are excluded.
- Do not change input objects or their nested values. Each call starts with fresh state.
