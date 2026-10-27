## Approach

The deque holds only accepted times inside the current window. Each call first
removes expired times from the left, then compares the remaining count with the limit. Every time
enters and leaves the deque once, so a call costs amortized O(1), and memory is O(limit).
Rejected calls are counted but not stored, so a burst of rejections cannot extend a block.

## Reference classes

```python
from collections import deque


class Throttle:
    def __init__(self, limit: int, window: int):
        if limit < 1 or window < 1:
            raise ValueError("limit and window must be at least 1")
        self.limit = limit
        self.window = window
        self._times: deque[int] = deque()
        self._accepted = 0
        self._rejected = 0

    def __call__(self, now: int) -> bool:
        while self._times and self._times[0] <= now - self.window:
            self._times.popleft()
        if len(self._times) < self.limit:
            self._times.append(now)
            self._accepted += 1
            return True
        self._rejected += 1
        return False

    @property
    def accepted(self) -> int:
        return self._accepted

    @property
    def rejected(self) -> int:
        return self._rejected

    def __repr__(self) -> str:
        return f"Throttle(limit={self.limit}, window={self.window})"
```
