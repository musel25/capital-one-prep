## Reference solution

```python
COLOR_NAMES = {
    "ALICEBLUE": (240, 248, 255),
    "AQUA": (0, 255, 255),
    "BLACK": (0, 0, 0),
    "BLUE": (0, 0, 255),
    "BROWN": (165, 42, 42),
    "CORAL": (255, 127, 80),
    "CRIMSON": (220, 20, 60),
    "CYAN": (0, 255, 255),
    "GOLD": (255, 215, 0),
    "GRAY": (128, 128, 128),
    "GREEN": (0, 128, 0),
    "INDIGO": (75, 0, 130),
    "IVORY": (255, 255, 240),
    "LAVENDER": (230, 230, 250),
    "LIME": (0, 255, 0),
    "MAGENTA": (255, 0, 255),
    "MAROON": (128, 0, 0),
    "NAVY": (0, 0, 128),
    "OLIVE": (128, 128, 0),
    "ORANGE": (255, 165, 0),
    "ORCHID": (218, 112, 214),
    "PINK": (255, 192, 203),
    "PURPLE": (128, 0, 128),
    "RED": (255, 0, 0),
    "SALMON": (250, 128, 114),
    "SILVER": (192, 192, 192),
    "TEAL": (0, 128, 128),
    "TOMATO": (255, 99, 71),
    "TURQUOISE": (64, 224, 208),
    "VIOLET": (238, 130, 238),
    "WHITE": (255, 255, 255),
    "YELLOW": (255, 255, 0),
}



class Color:
    """Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color):
        self.color = color
        self.rgb = COLOR_NAMES.get(color.upper())

    @staticmethod
    def hex2rgb(hex_value):
        if (not isinstance(hex_value, str) or len(hex_value) != 7 or hex_value[0] != "#"
                or any(ch not in "0123456789abcdefABCDEF" for ch in hex_value[1:])):
            raise ValueError(f"invalid hex value: {hex_value!r}")
        return tuple(int(hex_value[i:i + 2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb2hex(rgb_value):
        if (not isinstance(rgb_value, tuple) or len(rgb_value) != 3
                or any(type(v) is not int or not 0 <= v <= 255 for v in rgb_value)):
            raise ValueError(f"invalid rgb value: {rgb_value!r}")
        return "#" + "".join(f"{v:02x}" for v in rgb_value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color!r})"

    def __str__(self):
        return str(self.rgb) if self.rgb is not None else "Unknown"
```
