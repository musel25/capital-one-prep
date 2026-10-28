In this bite a real world scenario: *PyBites has a growing set of Bites and gives away promos.* They choose a Bite randomly but don't want to choose the same one again.

Hence you are provided with a `BITES dict` and a `BITES_DONE set` that we use (copies) in the `Promo` class via its constructor (code provided).

Complete the following methods in the Promo class:

1. `_pick_random_bite` is a helper (`_` here means "private", not to be called directly on an instance) that picks a randomly available Bite (use the `random` module).

When no more Bites are available raise the provided `NoBitesAvailable` custom exception.

1. `new_bite` should use this helper and update `self.bites_done` (*it keeps state*, the reason we used a class here).

See also the tests. We hope you learn a thing or two. Enjoy!

**Update** 4th of Nov 2020: we changed this Bite slightly to localize the Bite constants (thanks Kenneth). No worries: it's all done in the `__init__` constructor for you, you don't have to change anything there).

**Constraints:**

- Done IDs belong to the supplied catalog. Empty containers are valid inputs.
