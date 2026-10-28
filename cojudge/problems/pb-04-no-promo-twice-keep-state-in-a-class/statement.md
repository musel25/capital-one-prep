# 04. No promo twice, keep state in a class

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/no-promo-twice-keep-state-in-a-class/)

**Inputs and required behavior for this version:**

bites is a dict from integer IDs to title strings. bites_done is a set of IDs from that dict. Either argument can be None to use its supplied default. Empty containers are valid and must not select defaults. Copy the inputs. _pick_random_bite returns an available ID without changing state. new_bite uses that helper, adds the ID to bites_done and returns it. Both methods raise NoBitesAvailable when no IDs remain. IDs cannot repeat. No exact random order is required. Other types and done IDs outside the catalog are outside the contract; no validation is required for them.

<details>
<summary>Original bite description</summary>

In this bite a real world scenario: *PyBites has a growing set of Bites and gives away promos.* They choose a Bite randomly but don't want to choose the same one again.

Hence you are provided with a `BITES dict` and a `BITES_DONE set` that we use (copies) in the `Promo` class via its constructor (code provided).

Complete the following methods in the Promo class:

1. `_pick_random_bite` is a helper (`_` here means "private", not to be called directly on an instance) that picks a randomly available Bite (use the `random` module).

When no more Bites are available raise the provided `NoBitesAvailable` custom exception.

1. `new_bite` should use this helper and update `self.bites_done` (*it keeps state*, the reason we used a class here).

See also the tests. We hope you learn a thing or two. Enjoy!

**Update** 4th of Nov 2020: we changed this Bite slightly to localize the Bite constants (thanks Kenneth). No worries: it's all done in the `__init__` constructor for you, you don't have to change anything there).

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `promo`. **Run** checks the first three tests. **Submit** runs all
14. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
