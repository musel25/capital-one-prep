# 09. Use the ipinfo api to lookup ip country

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/use-the-ipinfo-api-to-lookup-ip-country/)

Implement `get_country(ip="8.8.8.8", client=None)`. Format `IPINFO_URL` with the given IP address. Call `client.get(url)`, call `json()` on its response, and return the `country` field. When `client` is None, use the supplied `requests` object. The field contains a two-character country code. Preserve its case. IP addresses are strings; IPv4 and IPv6 are accepted without validation. Make exactly one GET call per invocation. Missing country fields raise KeyError. Client and JSON errors pass through unchanged. Do not modify the response data. No network call is needed: `requests` is a local requests-compatible client with three sample records. Tests also inject clients with other records.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The public exercise uses requests. This version supplies a local object with the same get()/response.json() interface. An optional client parameter supports injection. The original premium template and tests are unavailable; these interfaces and tests are recreated.

<details>
<summary>Original public description</summary>

In this Bite you will use the `requests` library to make a *GET request* to the *ipinfo* service.

Use `IPINFO_URL` and parse the (2 char) country code from the obtained *json* response.

Note how we mocked out the `requests.get` call in the tests, you can see another example of this in our [Parsing Twitter Geo Data and Mocking API Calls by Example](https://pybit.es/articles/twitter-api-geodata-mocking/) article.

Querying APIs is a common need so this should become second nature :) - enjoy!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`ip_country`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
