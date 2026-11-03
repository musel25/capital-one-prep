**The ticket.** Servers in different time zones send event times with an offset, for example `2026-10-28T00:30:00+02:00`. The daily report must count events per UTC day.

**Why it matters.** If you take the date from the text, an event at 00:30 in Berlin counts for the wrong day. Daily totals then do not match other reports.

### Your task

Write `count_utc_days(timestamps)`. Return a dictionary from dates (`YYYY-MM-DD`) to counts.

1. Read each timestamp. `Z` means UTC. `+02:00` means two hours ahead of UTC.
2. Convert the time to UTC. Then take its date.
3. Count the events for each UTC date. Count duplicates separately.

Example: `2026-10-28T00:30:00+02:00` is `2026-10-27T22:30:00` in UTC, so it counts for `2026-10-27`.

**Constraints:**

- 0–200 timestamps in the form `YYYY-MM-DDTHH:MM:SS` followed by `Z`, `+HH:MM`, or `-HH:MM`.
- Input years are 2000–2099. The UTC date can be in 1999 or 2100.
