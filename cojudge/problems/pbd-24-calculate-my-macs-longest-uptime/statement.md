# 24. Calculate my mac's longest uptime

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/calculate-my-macs-longest-uptime/)

get_longest_uptime(text, year=2019) reads lines such as "reboot    ~    Wed Apr 10 22:39". All events belong to year. Sort events, then return the largest timedelta between adjacent events. Duplicate events are allowed. Fewer than two events returns timedelta(0). Ignore blank lines and non-reboot lines. Invalid reboot dates raise ValueError. Do not include the time since the last reboot. Year boundaries are outside this contract; the year argument supports leap years.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Given the following output, calculate the longest uptime / time between reboots:

```python
[bbelderbos@imac log]$ last reboot
reboot    ~                         Wed Apr 10 22:39
reboot    ~                         Wed Mar 27 16:24
reboot    ~                         Wed Mar 27 15:01
reboot    ~                         Sun Mar  3 14:51
reboot    ~                         Sun Feb 17 11:36
reboot    ~                         Thu Jan 17 21:54
reboot    ~                         Mon Jan 14 09:25

```

The tests will check your code against different `last reboot` outputs. You can assume all dates are within the same year.

Have fun and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`uptime`. **Run** checks the first three tests. **Submit** checks all 9 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
