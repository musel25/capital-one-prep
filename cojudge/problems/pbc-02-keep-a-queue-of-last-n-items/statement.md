# 02. Keep a queue of last n items

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/keep-a-queue-of-last-n-items/)

Implement `my_queue(n=5)`. Return an empty `collections.deque` with maximum length `n`. `n` is a nonnegative integer. Appends keep the newest `n` items in insertion order. A length of 0 discards every appended item.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

How about writing a *queue* that holds the last 5 items?

> Queue follows First-In-First-Out methodology, i.e., the data item stored first will be accessed first. A real-world example of queue can be a single-lane one-way road, where the vehicle enters first, exits first. More real-world examples can be seen as queues at the ticket windows and bus-stops. [[source](https://www.tutorialspoint.com/data_structures_algorithms/dsa_queue.htm)] Complete the `my_queue` function to return a queue-like data type that keeps the last `n` items.

Check the *standard library* to see how you can do this in the shortest/most efficient way.

See an example output below and the tests that check for various values of `n`. Have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`myqueue`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
