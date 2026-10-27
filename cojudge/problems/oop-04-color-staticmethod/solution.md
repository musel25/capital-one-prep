## Approach

`hex_to_rgb` validates every character instead of trusting `int(..., 16)`, which
accepts signs, spaces, and underscores. The constructor reuses it for validation. Both helpers
are static methods: they do not need an instance, and the class and its instances can call them.
`blend` builds the result through `rgb_to_hex`, so it returns a normal, validated `Color`.

## Reference classes

```python
HEX_DIGITS = "0123456789abcdefABCDEF"


class Color:
    def __init__(self, code: str):
        self.hex_to_rgb(code)
        self.hex = code.lower()

    @staticmethod
    def hex_to_rgb(code: str) -> tuple[int, int, int]:
        if len(code) != 7 or code[0] != "#" or any(ch not in HEX_DIGITS for ch in code[1:]):
            raise ValueError(f"invalid hex code: {code!r}")
        return tuple(int(code[i:i + 2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb_to_hex(red: int, green: int, blue: int) -> str:
        for value in (red, green, blue):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 255:
                raise ValueError(f"invalid component: {value!r}")
        return f"#{red:02x}{green:02x}{blue:02x}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.hex_to_rgb(self.hex)

    def blend(self, other: "Color") -> "Color":
        mixed = [(a + b) // 2 for a, b in zip(self.rgb, other.rgb)]
        return Color(self.rgb_to_hex(*mixed))

    def __repr__(self) -> str:
        return f"Color({self.hex!r})"
```
