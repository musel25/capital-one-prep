In this Bite you will use the `requests` library to make a *GET request* to the *ipinfo* service.

Use `IPINFO_URL` and parse the (2 char) country code from the obtained *json* response.

Note how we mocked out the `requests.get` call in the tests, you can see another example of this in our [Parsing Twitter Geo Data and Mocking API Calls by Example](https://pybit.es/articles/twitter-api-geodata-mocking/) article.

Querying APIs is a common need so this should become second nature :) - enjoy!

The supplied requests-compatible client returns local responses.

**Constraints:**

- Make one GET call and return the country unchanged; missing fields and client errors propagate.
