# 05. Test code that parses json and ip ranges

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/test-code-that-parses-json-and-ip-ranges/).

This is an offline recreation from the public description. The original code and template are premium and were not available. The API below belongs to this recreation.

## Contract

parse_ranges(text) parses a JSON object with a prefixes list. Each item has ip_prefix, region, and service. Return frozen IPRange dataclass objects in input order. Use strict IPv4Network parsing. get_ranges(path) reads UTF-8 JSON from a local file. filter_ranges applies optional exact region and service filters together. Propagate JSON, key, IP, and file errors.

## Code to test

Import this module as `ips`. The judge supplies it automatically.

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

## Your task

Scroll to **WRITE YOUR TESTS BELOW** in the editor. Replace the placeholder with `test_` functions. Keep the supplied target, runner, and adapter unchanged.

1. All tests must pass against the correct code.
2. Cover at least 90% of executable statements in the supplied target.
3. Detect every supplied faulty variant. A faulty variant is detected when at least one test fails against it.

**Run** checks the baseline and the first two faults. **Submit** checks the baseline and all 5 faults. `SURVIVED` identifies a fault your tests missed. A baseline failure shows the test name and error. Empty suites do not pass.

## Offline pytest support

The supplied runner implements the same small pytest subset used by the OOP course: `pytest.raises` (with `match`), `pytest.mark.parametrize`, function and yield fixtures, `pytest.approx` for numbers, `pytest.fail`, `capsys` / `capfd` for Python output, `monkeypatch`, and `tmp_path`. Standard-library `unittest.mock.patch` also works. Use function-scoped fixtures and top-level test functions. Plugins, async tests, pytest classes with setup hooks, skip/xfail, and advanced fixture scopes are not supported.

The judge uses Python 3.11 and no network. This runner measures statement coverage with Python tracing and uses explicit faulty variants. It does **not** run pytest-cov or mutatest. Its acceptance result is specific to this course.

For an older saved tab, use **+** to open the current template. Keep the old tab intact.
