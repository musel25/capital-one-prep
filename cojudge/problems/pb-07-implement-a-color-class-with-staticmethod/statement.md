As the new junior developer, you have been charged with enhancing the **Color** class.

Your task will be to implement the following:

- add `self.rgb` to the **__init__** method that gets its value from the provided `COLOR_NAMES` dictionary (k, v = color_name, rgb tuple = e.g.: `"ALICEBLUE": (240, 248, 255)`). If the value does not exist, just assume it is `None`.
- Convert `hex2rgb` and `rgb2hex` into `@staticmethod`s.
- Validate the values being passed to each of these *staticmethods* and raise a `ValueError` if called with bad data.
- Add a **__repr__** method whose value is in the form of `Color('white')`, with *white* being the inital value that it was initialized with.
- Add a **__str__** method whose value is the RGB value of the color if it is found in `COLOR_NAMES`, else return `Unknown`.

Take a look at the tests for a better understanding of the values expected.

Good luck!
