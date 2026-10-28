## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime
def get_shutdown_times(log):
    return [datetime.fromisoformat(line.split()[1]) for line in log.splitlines() if 'Shutdown initiated.' in line]
def get_time_between_shutdowns(log):
    times = get_shutdown_times(log)
    if len(times) < 2:
        raise ValueError('Need two shutdowns')
    return times[-1] - times[0]
```
