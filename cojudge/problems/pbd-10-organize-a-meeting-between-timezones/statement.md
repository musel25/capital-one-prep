# 10. Organize a meeting between timezones

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/organize-a-meeting-between-timezones/)

is_good_meeting_time(utc_datetime, timezones) returns True if local hours are in [MIN_MEETING_HOUR, MAX_MEETING_HOUR) for every IANA timezone. Constants are 9 and 18. A naive input is interpreted as UTC; an aware input is converted from its offset. Use zoneinfo, including daylight saving time. Empty zones returns True. An unknown timezone raises ValueError, even if another zone is outside meeting hours. The supplied ZoneInfo loader reads bundled IANA 2026b timezone data, including legacy aliases. Keep this supplied loader; it returns standard-library ZoneInfo objects.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

*We used pytz for this Bite before, but since 3.9 you can use the [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) (Standard lib) module 📈*

Help Pybites community friends find a reasonable common time to meet!

Complete the function below receiving a UTC `datetime` and one or more timezones (*US/Arizona*, *Europe/Madrid*, etc).

Use the `zoneinfo` module to see if the given datetime is within `MIN_MEETING_HOUR` and `MAX_MEETING_HOUR` for all provided timezones. Return a boolean.

If a wrong timezone is given raise a `ValueError`.

See the TESTS tab for `True`/`False` scenarios. Good luck and have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`meeting`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
