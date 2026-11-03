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
# What you practise
# -----------------
# A static method belongs to the class but gets no self and no cls. It is a
# plain function that lives inside the class, so you call it on the class:
#
#     Color.hex2rgb('#ff8000')   -> (255, 128, 0)    (no Color object needed)
#
# Put @staticmethod on the line above the def. It also works through an
# object: Color('red').hex2rgb('#00ff00').
#
# SUPPLIED: _is_hex and _is_rgb below do all the input validation. They are
# not the skill of this exercise. Use them. Do not edit them.
#
# Work in four steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (__init__)            -> test_rgb_from_color_names, test_unknown_color_has_no_rgb
#   Step 2 (__repr__, __str__)   -> test_repr, test_str
#   Step 3 (hex2rgb)             -> test_hex2rgb, test_hex2rgb_bad_values
#   Step 4 (rgb2hex)             -> test_rgb2hex and the tests after it


def _is_hex(value):
    """True only for '#' followed by six ASCII hex digits, such as '#FF8000'."""
    return (isinstance(value, str) and len(value) == 7 and value[0] == "#"
            and all(ch in "0123456789abcdefABCDEF" for ch in value[1:]))


def _is_rgb(value):
    """True only for a tuple of three ints from 0 to 255, such as (255, 128, 0). bool is not valid."""
    return (isinstance(value, tuple) and len(value) == 3
            and all(type(v) is int and 0 <= v <= 255 for v in value))


class Color:
    """Color class.

    Takes the string of a color name and returns its RGB value.
    """

    # Step 1: look up the name in COLOR_NAMES. The keys are UPPERCASE.
    #
    #     Color('Tomato').rgb   -> (255, 99, 71)
    #     Color('white').rgb    -> (255, 255, 255)
    #     Color('puke').rgb     -> None          (unknown name)
    #     Color(' white ').rgb  -> None          (do not strip spaces)
    def __init__(self, color):
        self.color = color   # keep the name exactly as given
        # TODO: set self.rgb = COLOR_NAMES.get(<color in uppercase>).
        #       dict.get returns None when the key is missing.
        ...

    # Step 2: the two text forms.
    #
    #     repr(Color('ToMaTo'))  -> "Color('ToMaTo')"   (name as given, in quotes)
    #     str(Color('navy'))     -> '(0, 0, 128)'       (str of the rgb tuple)
    #     str(Color('puke'))     -> 'Unknown'           (rgb is None)
    #
    # TODO: define __repr__(self). {self.color!r} in an f-string adds the quotes.
    # TODO: define __str__(self).

    # Step 3: hex text -> RGB tuple. Each pair of hex digits is one channel.
    #
    #     Color.hex2rgb('#FF8000')  -> (255, 128, 0)   ('FF', '80', '00')
    #     Color.hex2rgb('#fff')     -> raises ValueError (not 6 digits)
    #
    # TODO: put @staticmethod on the line above the def.
    def hex2rgb(hex_value):
        """Return a tuple of 3 ints. Raise ValueError if not _is_hex(hex_value)."""
        # TODO: if not _is_hex(hex_value): raise ValueError(...)
        # TODO: convert hex_value[1:3], [3:5] and [5:7] with int(pair, 16).
        ...

    # Step 4: RGB tuple -> lowercase hex text, two digits per channel.
    #
    #     Color.rgb2hex((255, 128, 0))  -> '#ff8000'
    #     Color.rgb2hex((10, 11, 12))   -> '#0a0b0c'   (keep the leading 0)
    #     Color.rgb2hex((256, 0, 0))    -> raises ValueError
    #
    # TODO: put @staticmethod on the line above the def.
    def rgb2hex(rgb_value):
        """Return '#rrggbb' in lowercase. Raise ValueError if not _is_rgb(rgb_value)."""
        # TODO: if not _is_rgb(rgb_value): raise ValueError(...)
        # TODO: format each channel with f'{v:02x}' and join them after '#'.
        ...
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

# FOCUS: write the two @staticmethod converters and the Color dunder methods by hand.
#        A static method gets no self and no cls: Color.hex2rgb('#ff8000') works.
# SUPPLIED: the two checks below do the input validation. They are not the skill
#        of this exercise. Use them. Do not edit them.


def _is_hex(value):
    """True only for '#' followed by six ASCII hex digits, such as '#FF8000'."""
    return (isinstance(value, str) and len(value) == 7 and value[0] == "#"
            and all(ch in "0123456789abcdefABCDEF" for ch in value[1:]))


def _is_rgb(value):
    """True only for a tuple of three ints from 0 to 255, such as (255, 128, 0). bool is not valid."""
    return (isinstance(value, tuple) and len(value) == 3
            and all(type(v) is int and 0 <= v <= 255 for v in value))


class Color:
    """Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color):
        self.color = color
        self.rgb = COLOR_NAMES.get(color.upper())

    @staticmethod
    def hex2rgb(hex_value):
        if not _is_hex(hex_value):
            raise ValueError(f"invalid hex value: {hex_value!r}")
        return tuple(int(hex_value[i:i + 2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb2hex(rgb_value):
        if not _is_rgb(rgb_value):
            raise ValueError(f"invalid rgb value: {rgb_value!r}")
        return "#" + "".join(f"{v:02x}" for v in rgb_value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color!r})"

    def __str__(self):
        return str(self.rgb) if self.rgb is not None else "Unknown"
''',
}

SPEC["contract"] = (
    "Color receives a string name. Lookup is case-insensitive and uses only the "
    "supplied COLOR_NAMES. Empty and unknown names have rgb None; str returns "
    "'Unknown'. Known names produce their RGB tuple as a string. repr preserves "
    "the initial name and case, as in Color('white'). Non-string constructor "
    "arguments are outside the contract. hex2rgb accepts exactly '#' followed by "
    "six ASCII hex digits and returns three integers. rgb2hex accepts exactly a "
    "three-item tuple of int values from 0 through 255; bool is invalid. It returns "
    "'#rrggbb' in lowercase. Both static methods raise ValueError for all other "
    "inputs. They also work through an instance."
)
SPEC["tests"] += '''


@pytest.mark.parametrize('name', ['', ' white ', 'not-a-color'])
def test_unknown_names_are_not_normalized(name):
    color = Color(name)
    assert color.rgb is None
    assert str(color) == 'Unknown'


def test_repr_preserves_original_case():
    assert repr(Color('ToMaTo')) == "Color('ToMaTo')"


@pytest.mark.parametrize('bad', [
    '', '#', '#12345', '#1234567', '# 12345', '#+12345', '#１２３４５６',
    '#12345\\n', ' #123456', '#123456 ', b'#123456', [], {}, True,
])
def test_hex2rgb_rejects_malformed_values(bad):
    with pytest.raises(ValueError):
        Color.hex2rgb(bad)


@pytest.mark.parametrize('bad', [
    [0, 0, 0], {0: 0, 1: 0, 2: 0}, (), (True, 0, 0), (0, False, 0),
    (0, 0, True), (-1, 0, 0), (0, 256, 0), (0, 0, -1), (0, 0, 256),
    ('1', 0, 0), (0, 0.0, 0), (0, 0, None),
])
def test_rgb2hex_rejects_wrong_container_and_channel_values(bad):
    with pytest.raises(ValueError):
        Color.rgb2hex(bad)


def test_asymmetric_channels_and_both_instance_converters():
    color = Color('red')
    assert color.hex2rgb('#0102Fe') == (1, 2, 254)
    assert color.rgb2hex((1, 2, 254)) == '#0102fe'


def test_every_supplied_name_resolves_to_its_literal_rgb():
    for name, rgb in COLOR_NAMES.items():
        assert Color(name.lower()).rgb == rgb
'''
SPEC["hints"] = [
    "Concept: @staticmethod makes a method that gets no self. Write @staticmethod above def hex2rgb and def rgb2hex, with only the value as the parameter. Then Color.hex2rgb('#ff8000') works without an object.",
    'Lookup and text forms: self.rgb = COLOR_NAMES.get(color.upper()). __repr__ returns f"Color({self.color!r})". __str__ returns str(self.rgb), or \'Unknown\' when self.rgb is None.',
    "Conversion: call the supplied check first and raise ValueError when it returns False. int('ff', 16) == 255, and f'{255:02x}' == 'ff'. The :02x format keeps a leading zero: f'{10:02x}' == '0a'.",
]
SPEC["mutations"] = [
    {"name": "case-sensitive color lookup", "old": "COLOR_NAMES.get(color.upper())", "new": "COLOR_NAMES.get(color)"},
    {"name": "hex2rgb is not a static method", "old": "    @staticmethod\n    def hex2rgb", "new": "    def hex2rgb"},
    {"name": "rgb2hex is not a static method", "old": "    @staticmethod\n    def rgb2hex", "new": "    def rgb2hex"},
    {"name": "skip hex validation", "old": "if not _is_hex(hex_value):", "new": "if False:"},
    {"name": "skip rgb validation", "old": "if not _is_rgb(rgb_value):", "new": "if False:"},
    {"name": "drop hex zero padding", "old": "f\"{v:02x}\"", "new": "f\"{v:x}\""},
    {"name": "reverse hex channels", "old": "for i in (1, 3, 5)", "new": "for i in (5, 3, 1)"},
]
