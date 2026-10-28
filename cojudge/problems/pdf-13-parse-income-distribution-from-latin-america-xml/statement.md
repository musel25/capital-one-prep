In this Bite you are going to parse some Latin American countries in `xml`, specifically the output of *[api.worldbank.org/V2/country?region=LCN](http://api.worldbank.org/V2/country?region=LCN)* which we stored [here](https://bites-data.s3.us-east-2.amazonaws.com/countries.xml). It's already saved for you in the `countries` temp file.

Complete `get_income_distribution` by reading in this file, parsing its XML and returning a `dict` of keys = wb:incomeLevel and values = `list`s of country names (wb:name). `defaultdict` is a convenient data structure to use here. See also the tests for the expected return.

Good luck and code more Python!

The supplied XML is a small constructed sample, rather than current income classifications.

**Constraints:**

- Group by income label text, not the ID; preserve country order and duplicates.
- All country entries have nonempty names and labels in the World Bank namespace.
