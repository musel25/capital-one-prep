*Update 2026: original Bite text left intact. We no longer have a Slack (nor Circle) community, but that does not affect doing this exercise.*

We played a bit with the Slack API the other day and wow: our Pybites community is super international! We really enjoy connecting with Pythonistas from all over the globe.

We put some anonymized data in a csv (using `uuid4` and `faker`) and for this Bite we ask you to use `requests` to load it in, use the `csv` module to parse it into a data structure of your choice, and finally **print** the following output to the screen:

```python
Africa/Algiers       | ++
Africa/Cairo         | +
Africa/Monrovia      | +
Africa/Nairobi       | ++++
...
...
Europe/Moscow        | ++
Europe/Warsaw        | ++
Pacific/Honolulu     | +

```

See the full output under the TESTS tab. Good luck and remember: keep calm and code in Python!

The supplied CSV text replaces the network download.

**Constraints:**

- `create_bar_chart` receives CSV text with a `timezone` column; ignore blank timezone values.
- Sort timezones; use a column width of at least 20, expanded for longer names; print one `+` per record.
