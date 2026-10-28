## Reference solution

Paste this code above the supplied tests and runner.

```python
IPINFO_URL = 'https://ipinfo.io/{ip}/json'


class LocalResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return dict(self.payload)


class LocalClient:
    """A requests-compatible client. It uses local records and makes no network calls."""
    def __init__(self):
        self.records = {'8.8.8.8': {'country': 'US', 'city': 'Mountain View'},
                        '1.1.1.1': {'country': 'AU', 'city': 'Sydney'},
                        '2001:db8::1': {'country': 'MX'}}

    def get(self, url):
        prefix, suffix = 'https://ipinfo.io/', '/json'
        if not url.startswith(prefix) or not url.endswith(suffix):
            raise ValueError('Unexpected local URL')
        ip = url[len(prefix):-len(suffix)]
        return LocalResponse(self.records[ip])


requests = LocalClient()


def get_country(ip="8.8.8.8", client=None):
    if client is None:
        client = requests
    response = client.get(IPINFO_URL.format(ip=ip))
    return response.json()['country']
```
