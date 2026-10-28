# 06. Parsing dates from logs

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/parsing-dates-from-logs/)

get_shutdown_times(log) extracts naive datetime timestamps from lines containing "Shutdown initiated.". Lines use LEVEL YYYY-MM-DDTHH:MM:SS text and are in ascending time order. get_time_between_shutdowns(log) returns the timedelta between first and last shutdown. Raise ValueError if there are fewer than two shutdowns. Unrelated lines are ignored.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite we will look at this short server [log](https://bites-data.s3.us-east-2.amazonaws.com/messages.log), finding the **first **and **last** system shutdown events:

```python
INFO 2014-07-03T23:27:51 supybot Shutdown initiated.
...
INFO 2014-07-03T23:31:22 supybot Shutdown initiated.
```

You'll need to calculate the time between these two events. First extract the timestamps from the log entries and convert them to `datetime` objects. Then use `datetime.timedelta` to calculate the time difference between them.

You can assume the log is sorted in ascending order. Check out each function's `docstring` and the **TESTS** for more details on how to solve this Bite.

Good luck, keep calm, and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`shutdowns`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
