*We used pytz for this Bite before, but since 3.9 you can use the [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) (Standard lib) module 📈*

Help Pybites community friends find a reasonable common time to meet!

Complete the function below receiving a UTC `datetime` and one or more timezones (*US/Arizona*, *Europe/Madrid*, etc).

Use the `zoneinfo` module to see if the given datetime is within `MIN_MEETING_HOUR` and `MAX_MEETING_HOUR` for all provided timezones. Return a boolean.

If a wrong timezone is given raise a `ValueError`.

See the TESTS tab for `True`/`False` scenarios. Good luck and have fun!

Use the supplied offline `ZoneInfo` loader and the standard library.

**Constraints:**

- Local hours must be at least 9 and less than 18; a naive datetime means UTC.
- An empty timezone list returns `True`; validate every timezone before checking hours.
