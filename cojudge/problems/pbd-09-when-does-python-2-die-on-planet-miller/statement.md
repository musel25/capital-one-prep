# 09. When does python 2 die on planet miller?

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/when-does-python-2-die-on-planet-miller/)

BITE_CREATED_DT is 2018-02-26 00:00; PY2_DEATH_DT is 2020-01-01 00:00. calc_hours_left(start=BITE_CREATED_DT, end=PY2_DEATH_DT) returns Earth hours as float. calc_minutes_miller with the same arguments returns Miller minutes: Earth hours / (365 * 24 * 7) * 60. Use exactly 365 days per Earth year. Reject end before start.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Imagine you landed on *Planet Miller* (from the movie [Interstellar](http://www.imdb.com/title/tt0816692/?ref_=nv_sr_1)) **where 1 hour takes 7 Earth years** (known as the *gravitational time dilation effect* - see [here](https://www.quora.com/Interstellar-2014-movie-Why-did-every-hour-on-the-first-planet-take-7-years-on-Earth) if interested).

Given a fixed start date `BITE_CREATED_DT` (26th of Feb 2018) calculate:

1. How many hours Python 2 has left on Planet Earth
1. How many minutes Python 2 has left on Planet Miller

As per [pythonclock.org](https://pythonclock.org/) Python 2.7 will retire on 1st of Jan 2020 (after this date you can still do this Bite because we work a fixed start date.)

Have fun and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`miller`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
