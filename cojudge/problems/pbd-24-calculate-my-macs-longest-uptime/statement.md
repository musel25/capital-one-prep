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

**Constraints:**

- `get_longest_uptime(text, year=2019)` returns the largest gap as a `timedelta`; fewer than two reboots returns zero.
- Ignore non-reboot lines and sort reboot times before calculating gaps.
