In this Bite you read in a text file with course times (*MM:SS*) per video.

You extract these and calculate the total course duration in *HH:MM:SS*.

See the *docstrings* and tests for more details.

Have fun and we hope you learn a thing or two.

> Trivia: in honor of our [Code Challenges Pilot](https://pybit.es/articles/js_time_scraper_ch/): this was the exercise we used to test the waters when we started out :)

**Constraints:**

- Pass file contents as text; nonblank lines end in MM:SS, with minutes unrestricted and seconds 00–59.
- Empty text returns `00:00:00`; invalid lines raise `ValueError`.
