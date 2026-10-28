# 11. Cached property decorator

Implement `cached_property` in `cached`.

The first successful access computes and stores the value for that instance.
Later accesses return the stored value, including false or empty values. A
failed computation must allow another attempt. Keep separate caches for each
instance and each property. Preserve the decorated method's docstring.

This local API is read-only: assignment and deletion must raise `AttributeError`
before and after the first access. Direct changes to `__dict__` and objects
without `__dict__` are outside the exercise.

The supplied `Planet` class represents an expensive mass calculation without
waiting or external data. After `earth = Planet('Earth', 5.97)`, repeated reads
of `earth.mass` return `5.97` and call `earth._compute_mass()` only once.
