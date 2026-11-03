As the new junior developer, you have been charged with enhancing the **Color** class.

Your task will be to implement the following:

- add `self.rgb` to the **__init__** method that gets its value from the provided `COLOR_NAMES` dictionary (k, v = color_name, rgb tuple = e.g.: `"ALICEBLUE": (240, 248, 255)`). If the value does not exist, just assume it is `None`.
- Convert `hex2rgb` and `rgb2hex` into `@staticmethod`s.
- Validate the values being passed to each of these *staticmethods* and raise a `ValueError` if called with bad data.
- Add a **__repr__** method whose value is in the form of `Color('white')`, with *white* being the inital value that it was initialized with.
- Add a **__str__** method whose value is the RGB value of the color if it is found in `COLOR_NAMES`, else return `Unknown`.

Take a look at the tests for a better understanding of the values expected.

Good luck!

**Constraints:**

- `Color(name).rgb` is the `COLOR_NAMES` value for `name.upper()`, or `None`. `str()` returns the tuple as text or `Unknown`. `repr()` returns `Color(<name as given, quoted>)`.
- `hex2rgb` and `rgb2hex` are static methods. `rgb2hex` returns `#rrggbb` in lowercase. Both raise `ValueError` when the supplied `_is_hex` or `_is_rgb` check fails.
