Another Test Bite, we ❤️them 😁- today you will write tests for IPv4Network (ipaddress module) and dataclass objects 💪. Check out the ips module I wrote parsing a JSON file of IP ranges (ip-ranges.json) under CODE TO TEST, then write tests to get to 100% test coverage and a 100% mutation score.

Good luck and keep calm and code in Python 🐍 and pytest. Share your accomplishment upon completing the Bite 😎

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `ips`. The judge supplies it automatically.

```python
import json
from dataclasses import dataclass
from ipaddress import IPv4Network

@dataclass(frozen=True)
class IPRange:
    network: IPv4Network
    region: str
    service: str

def parse_ranges(text):
    return [IPRange(IPv4Network(item['ip_prefix']), item['region'], item['service'])
            for item in json.loads(text)['prefixes']]

def get_ranges(path):
    with open(path, encoding='utf-8') as stream:
        return parse_ranges(stream.read())

def filter_ranges(ranges, region=None, service=None):
    return [item for item in ranges
            if (region is None or item.region == region)
            and (service is None or item.service == service)]
```
