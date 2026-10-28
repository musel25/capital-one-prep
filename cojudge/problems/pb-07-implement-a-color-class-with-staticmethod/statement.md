# 07. Implement a color class with staticmethod

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/implement-a-color-class-with-staticmethod/)

**Inputs and required behavior for this version:**

Color receives a string name. Lookup is case-insensitive and uses only the supplied COLOR_NAMES. Empty and unknown names have rgb None; str returns 'Unknown'. Known names produce their RGB tuple as a string. repr preserves the initial name and case, as in Color('white'). Non-string constructor arguments are outside the contract. hex2rgb accepts exactly '#' followed by six ASCII hex digits and returns three integers. rgb2hex accepts exactly a three-item tuple of int values from 0 through 255; bool is invalid. It returns '#rrggbb' in lowercase. Both static methods raise ValueError for all other inputs. They also work through an instance.

<details>
<summary>Original bite description</summary>

As the new junior developer, you have been charged with enhancing the **Color** class.

Your task will be to implement the following:

- add `self.rgb` to the **__init__** method that gets its value from the provided `COLOR_NAMES` dictionary (k, v = color_name, rgb tuple = e.g.: `"ALICEBLUE": (240, 248, 255)`). If the value does not exist, just assume it is `None`.
- Convert `hex2rgb` and `rgb2hex` into `@staticmethod`s.
- Validate the values being passed to each of these *staticmethods* and raise a `ValueError` if called with bad data.
- Add a **__repr__** method whose value is in the form of `Color('white')`, with *white* being the inital value that it was initialized with.
- Add a **__str__** method whose value is the RGB value of the color if it is found in `COLOR_NAMES`, else return `Unknown`.

Take a look at the tests for a better understanding of the values expected.

Good luck!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `color`. **Run** checks the first three tests. **Submit** runs all
63. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
