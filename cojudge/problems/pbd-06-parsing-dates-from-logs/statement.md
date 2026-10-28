In this Bite we will look at this short server [log](https://bites-data.s3.us-east-2.amazonaws.com/messages.log), finding the **first **and **last** system shutdown events:

```python
INFO 2014-07-03T23:27:51 supybot Shutdown initiated.
...
INFO 2014-07-03T23:31:22 supybot Shutdown initiated.
```

You'll need to calculate the time between these two events. First extract the timestamps from the log entries and convert them to `datetime` objects. Then use `datetime.timedelta` to calculate the time difference between them.

You can assume the log is sorted in ascending order. Check out each function's `docstring` and the **TESTS** for more details on how to solve this Bite.

Good luck, keep calm, and code in Python!

**Constraints:**

- Pass log text directly; ignore unrelated lines and raise `ValueError` for fewer than two shutdowns.
