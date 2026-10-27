# 13. Keep an account balance nonnegative

[Course list](/?course=capital-one-engineering-50) · Level 2 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Classes, methods, and integer cents.

An invariant is a rule that must hold after every operation. Here the balance must never become negative. Put balance changes inside account methods so the rule has one enforcement point. A property can expose the current balance without providing a public setter. A leading underscore marks an internal attribute by Python convention; it is not a security barrier. Check a withdrawal before changing state. If it fails, the method should return a failure result and leave the balance unchanged. Keeping this rule in the object makes the calling loop simple and gives future operations a clear place to enforce the same invariant.

</details>

**Input:** `data` has:
- `balance`: a nonnegative integer number of cents.
- `actions`: a list of `{"op": "deposit" | "withdraw", "cents": int}`, with nonnegative `cents`.

**Rules**
- A deposit always succeeds.
- A withdrawal succeeds only when `cents` is at most the current balance. A failed withdrawal changes nothing.
- Zero-cent actions succeed.

**Return** `{"accepted": [bool], "balance": int}`: one boolean per action, and the final balance.

**Practice:** write an `Account` class that controls balance updates. The judge checks only the output.

**Constraints:**

- At most 100 actions. Initial balance and action cents are at most 1,000,000,000,000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/tutorial/classes.html#private-variables), [2](https://docs.python.org/3.11/library/functions.html#property)
