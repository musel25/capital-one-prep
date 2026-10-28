# 13. Parse income distribution from latin america xml

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/parse-income-distribution-from-latin-america-xml/)

Implement `get_income_distribution(path=None)`. When path is given, read that XML file (a string path or pathlib.Path). Otherwise parse COUNTRIES_XML, the supplied local sample. The root is a World Bank countries element. Its direct country children each have direct name and incomeLevel children in namespace `http://www.worldbank.org`. Return a dictionary mapping incomeLevel text labels to lists of country names. Strip surrounding whitespace from names and labels. Use the label text, not the incomeLevel id attribute. Preserve country order within each list and retain duplicate entries. A root without countries returns an empty dictionary. Return fresh dictionaries and lists on each call. A dict or defaultdict(list) is accepted. Namespace prefixes can differ. All country entries have nonempty names and income labels. Propagate XML parse and file errors. The original remote file is replaced by a small synthetic sample; these labels are exercise data, not current financial classifications.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you are going to parse some Latin American countries in `xml`, specifically the output of *[api.worldbank.org/V2/country?region=LCN](http://api.worldbank.org/V2/country?region=LCN)* which we stored [here](https://bites-data.s3.us-east-2.amazonaws.com/countries.xml). It's already saved for you in the `countries` temp file.

Complete `get_income_distribution` by reading in this file, parsing its XML and returning a `dict` of keys = wb:incomeLevel and values = `list`s of country names (wb:name). `defaultdict` is a convenient data structure to use here. See also the tests for the expected return.

Good luck and code more Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`income_distribution`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
