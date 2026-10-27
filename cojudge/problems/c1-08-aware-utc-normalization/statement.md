# 08. Normalize aware timestamps to UTC

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

An aware datetime has a time zone offset. It identifies an instant rather than an unqualified wall-clock reading. To express that instant in another time zone, use astimezone. Replacing tzinfo changes the label without adjusting the clock and usually changes the instant. An offset conversion can move the date to the previous or next day. Fixed offsets already contain the information needed for this task. They do not require local time zone rules. Parse each timestamp, convert it to UTC, and format all outputs in one consistent form. Preserve the input order because normalization does not imply sorting.

</details>

**Scenario:** A travel company receives booking times from partners in many time zones. Each time has an offset, such as `-07:00`. The company's database stores all times in UTC. `solve` converts each timestamp to UTC.

**Input:** `data` has:
- `timestamps`: a list of valid strings, each in one of these forms:
  - `YYYY-MM-DDTHH:MM:SSZ`
  - `YYYY-MM-DDTHH:MM:SS±HH:MM`, with an offset from `-14:00` to `+14:00`

Years are 2000–2099. All dates and times are valid. There are no leap seconds, no fractional seconds, and no zone names such as `America/Tijuana`.

**Return** the same instants converted to UTC, in input order, each as `YYYY-MM-DDTHH:MM:SSZ`. A UTC result can fall outside 2000–2099.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/datetime.html#datetime.datetime.astimezone)
