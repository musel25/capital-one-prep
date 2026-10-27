"""Bite: Implement a color class with staticmethod (recreated tests and template)."""

_NAMES = '''COLOR_NAMES = {
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
'''

SPEC = {
    "title": "Implement a color class with staticmethod",
    "module": "color",
    "template": _NAMES + '''

class Color:
    """Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color):
        self.color = color

    def hex2rgb(hex_value):
        """Convert a hex value such as '#ff8000' (any case) into an
           RGB tuple such as (255, 128, 0).
           Raise ValueError for anything else."""
        pass

    def rgb2hex(rgb_value):
        """Convert an RGB tuple such as (255, 128, 0) into a lowercase
           hex value such as '#ff8000'. Each part is an int from 0 to 255.
           Raise ValueError for anything else."""
        pass
''',
    "tests": '''import pytest

from color import COLOR_NAMES, Color


@pytest.mark.parametrize("name, rgb", [
    ("white", (255, 255, 255)),
    ("ALICEBLUE", (240, 248, 255)),
    ("Tomato", (255, 99, 71)),
])
def test_rgb_from_color_names(name, rgb):
    assert Color(name).rgb == rgb


def test_unknown_color_has_no_rgb():
    assert Color("puke").rgb is None


def test_repr():
    assert repr(Color("white")) == "Color('white')"
    assert repr(Color("puke")) == "Color('puke')"


def test_str():
    assert str(Color("white")) == "(255, 255, 255)"
    assert str(Color("navy")) == "(0, 0, 128)"
    assert str(Color("puke")) == "Unknown"


@pytest.mark.parametrize("hex_value, rgb", [
    ("#000000", (0, 0, 0)),
    ("#ffffff", (255, 255, 255)),
    ("#FF8000", (255, 128, 0)),
    ("#0a0B0c", (10, 11, 12)),
])
def test_hex2rgb(hex_value, rgb):
    assert Color.hex2rgb(hex_value) == rgb


@pytest.mark.parametrize("rgb, hex_value", [
    ((0, 0, 0), "#000000"),
    ((255, 255, 255), "#ffffff"),
    ((255, 128, 0), "#ff8000"),
    ((10, 11, 12), "#0a0b0c"),
])
def test_rgb2hex(rgb, hex_value):
    assert Color.rgb2hex(rgb) == hex_value


@pytest.mark.parametrize("bad", ["ffffff", "#fff", "#fffffff", "#gggggg", "#12_456", 123456, None])
def test_hex2rgb_bad_values(bad):
    with pytest.raises(ValueError):
        Color.hex2rgb(bad)


@pytest.mark.parametrize("bad", [(256, 0, 0), (0, -1, 0), (0, 0), (0, 0, 0, 0), "#ffffff", (1.5, 0, 0), None])
def test_rgb2hex_bad_values(bad):
    with pytest.raises(ValueError):
        Color.rgb2hex(bad)


def test_staticmethods():
    assert isinstance(Color.__dict__["hex2rgb"], staticmethod)
    assert isinstance(Color.__dict__["rgb2hex"], staticmethod)
    # static methods also work through an instance
    assert Color("red").hex2rgb("#00ff00") == (0, 255, 0)


def test_round_trip_all_names():
    for name, rgb in COLOR_NAMES.items():
        assert Color.hex2rgb(Color.rgb2hex(rgb)) == rgb
''',
    "reference": _NAMES + '''

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
''',
}
