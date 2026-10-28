`ABC`'s or `Abstract Base Classes` are great to enforce a common *API* for your subclasses.

You define one or more methods and/or properties as abstract in the base class, and if the subclass does not implement them it raises a `TypeError`. In this bite you will use this concept as follows:

1. Define a Challenge base class that inherits from `ABC` (given), its constructor receives a `number` and a `title` attribute.
1. On Challenge define an `abstractmethod` called `verify` and a `property` (< 3.3 it would be an `abstractproperty`) called `pretty_title`.
1. Create the `BlogChallenge` and `BiteChallenge` classes which both inherit from `Challenge`. *Note that they would raise a `TypeError` at this point, exactly what you want: enforcing the use of the abstract method/ property.*
1. `BlogChallenge` and `BiteChallenge`'s constructors call the parent constructor (don't worry it's *super*cool, remember: **we use Python3** so adjust your syntax), and both receive an extra argument in the constructor: `merged_prs` for `BlogChallenge` and `result` for `BiteChallenge`.
1. Implement the required methods and properties, refer to the tests what they need to return.

Get coding, learn more about classes, and have fun!
