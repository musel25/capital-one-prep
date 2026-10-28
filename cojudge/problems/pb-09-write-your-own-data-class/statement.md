As you might have noticed we are now on Python 3.7 so time for a Bite on *data classes* which were introduced with [PEP 557](https://www.python.org/dev/peps/pep-0557/).

What are they? Raymond Hettinger summarized it nicely [in his great talk](https://www.youtube.com/watch?v=T-TwcmT6Rcw): *a mutible named tuple with defaults*.

One advantage is the code it saves you typing so they might become an essential part of your Python toolkit!

In this Bite we have you write a data class called `Bite` that managed 3 attributes: *number*, *title*, and *level*. Their types are `int`, `str` and `str` respectively.

There are 3 more requirements:

1. *title* needs to be capitalized upon instantiation (you get a hint in the tests for this one :) - make sure to read the tests for additonal specs, including some of the differences between `data class`es and `namedtuple`s!)
1. *level* takes a default argument of *Beginner*.
1. A collection of Bite instances needs to be orderable (using `sort` / `sorted` - this is not by default but configurable ...)

Good luck and keep up with the language, exciting new things are getting added!
On that note feel free to make us more Bite requests via our Bites homepage (you'll find a form per Bite level at the bottom of the page ...)

For more resources on *data classes* we recommned watching [Hettinger's talk](https://www.youtube.com/watch?v=T-TwcmT6Rcw) as well as reading through Anthony Shaw's [A brief tour of Python 3.7 data classes](https://hackernoon.com/a-brief-tour-of-python-3-7-data-classes-22ee5e046517). Have fun!
