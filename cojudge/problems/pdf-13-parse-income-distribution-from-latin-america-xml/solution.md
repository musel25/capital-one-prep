## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import defaultdict
import xml.etree.ElementTree as ET

NAMESPACE = {'wb': 'http://www.worldbank.org'}
COUNTRIES_XML = '<?xml version="1.0" encoding="utf-8"?>\n<wb:countries xmlns:wb="http://www.worldbank.org" page="1" pages="1">\n  <wb:country id="ARG"><wb:name>Argentina</wb:name><wb:incomeLevel id="UMC">Upper middle income</wb:incomeLevel></wb:country>\n  <wb:country id="CHL"><wb:name>Chile</wb:name><wb:incomeLevel id="HIC">High income</wb:incomeLevel></wb:country>\n  <wb:country id="BOL"><wb:name>Bolivia</wb:name><wb:incomeLevel id="LMC">Lower middle income</wb:incomeLevel></wb:country>\n  <wb:country id="BRA"><wb:name>Brazil</wb:name><wb:incomeLevel id="UMC">Upper middle income</wb:incomeLevel></wb:country>\n  <wb:country id="URY"><wb:name>Uruguay</wb:name><wb:incomeLevel id="HIC">High income</wb:incomeLevel></wb:country>\n</wb:countries>\n'


def get_income_distribution(path=None):
    root = ET.fromstring(COUNTRIES_XML) if path is None else ET.parse(path).getroot()
    distribution = defaultdict(list)
    for country in root.findall('wb:country', NAMESPACE):
        name = country.find('wb:name', NAMESPACE).text.strip()
        income = country.find('wb:incomeLevel', NAMESPACE).text.strip()
        distribution[income].append(name)
    return dict(distribution)
```
