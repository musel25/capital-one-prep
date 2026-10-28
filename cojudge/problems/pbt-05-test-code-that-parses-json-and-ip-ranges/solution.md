## Reference tests

```python
import json
from ipaddress import IPv4Network
import pytest
from ips import IPRange, parse_ranges, get_ranges, filter_ranges

@pytest.fixture
def ranges(tmp_path):
    path = tmp_path / 'ranges.json'
    path.write_text(json.dumps({'prefixes': [
        {'ip_prefix': '10.0.0.0/24', 'region': 'west', 'service': 'EC2'},
        {'ip_prefix': '192.0.2.0/24', 'region': 'east', 'service': 'S3'},
        {'ip_prefix': '198.51.100.0/24', 'region': 'west', 'service': 'S3'}]}))
    return get_ranges(path)

def test_parse(ranges):
    assert ranges[0] == IPRange(IPv4Network('10.0.0.0/24'), 'west', 'EC2')
    assert len(ranges) == 3
    assert parse_ranges('{"prefixes": []}') == []
    assert len(filter_ranges(ranges)) == 3
    assert filter_ranges(ranges, region='west') == [ranges[0], ranges[2]]
    assert filter_ranges(ranges, service='S3') == [ranges[1], ranges[2]]
    assert filter_ranges(ranges, region='west', service='S3') == [ranges[2]]
    assert filter_ranges(ranges, region='missing') == []

def test_errors():
    with pytest.raises(ValueError):
        parse_ranges('broken')
    with pytest.raises(KeyError):
        parse_ranges('{}')
    with pytest.raises(ValueError):
        parse_ranges('{"prefixes": [{"ip_prefix": "invalid", "region": "x", "service": "y"}]}')
```
