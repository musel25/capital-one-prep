# 18. Parse pybites blog git commit log

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/parse-pybites-blog-git-commit-log/)

get_min_max_amount_of_commits(log, year=None) parses nonblank git-stat rows of the form "Date: Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+), 3 deletions(-)". Sum insertions plus deletions by YYYY-MM in the printed local date. A missing insertion/deletion term counts as zero. Ignore file counts. Optional year filters months. Return (least_month, most_month), selecting the earliest month for ties in either position. No matching rows returns (None, None). Malformed rows raise ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite we want to figure out how active we've been on our blog.

To start our data analysis we ran the following command on our [blog repo](https://github.com/pybites/pybites.github.io-src/commits/master): `git log --stat | egrep "^Date|file.*changed," |grep -B1 changed|grep -v '\-\-'|sed 'N;s/\n/ |/'` which resulted in the [following log](https://bites-data.s3.us-east-2.amazonaws.com/git_log_stat.out) which should be easier to work with:

```python
Date:   Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+), 4 deletions(-)
Date:   Tue Mar 5 20:34:34 2019 +0100 | 1 file changed, 2 insertions(+), 2 deletions(-)
Date:   Tue Mar 5 19:02:56 2019 +0100 | 2 files changed, 31 insertions(+), 2 deletions(-)
Date:   Tue Mar 5 14:18:55 2019 +0100 | 3 files changed, 3 insertions(+), 3 deletions(-)
Date:   Tue Mar 5 14:03:55 2019 +0100 | 2 files changed, 51 insertions(+), 39 deletions(-)
Date:   Tue Mar 5 13:23:51 2019 +0100 | 4 files changed, 109 insertions(+), 94 deletions(-)
...
[930 rows more]
...

```

Complete `get_min_max_amount_of_commits`, parsing this file into a `dict` where keys are year/months and values are the total number of changes as measured by # insertions + # deletions (number of file changes can be ignored).

For date parsing you can use the `datetime` or `dateutil` module. See the provided `YEAR_MONTH` constant for the exact format.

Return a tuple of (least_active_month, most_active_month).

Your code should work if we call it for a smaller data set as well. So if we pass in the optional `year` arg of 2018, it should give the min and max month only for that year (see also the tests).

By the way, with a min, max of `('2019-01', '2019-03')`, this year's trend is looking pretty good so far :)

Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`commit_log`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
