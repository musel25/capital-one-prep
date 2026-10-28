Write a function that returns the most common (non stop)word in [this Harry Potter text](https://bites-data.s3.us-east-2.amazonaws.com/harry.txt).

Make sure you convert to lowercase, strip out *non-alphanumeric* characters and [stopwords](https://bites-data.s3.us-east-2.amazonaws.com/stopwords.txt). Your function should return a *tuple* of (`most_common_word`, `frequency`).

The template code already loads the Harry Potter text and list of stopwords in.

Check the tests for more info - have fun!

**Constraints:**

- Split on whitespace, then remove non-alphanumeric characters. Ties keep first appearance order.
