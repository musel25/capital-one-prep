Now that you can insert workouts and exercises, the gym staff needs to retrieve them. Time to learn how to query your database!
In SQLModel, you build queries using the select() function. Think of it like asking the database a question: "Give me all workouts" or "Find the exercise named 'Squats'".

**Constraints:**

- Implement `get_workouts(session)`, `get_workout(session, workout_id)`, and `find_exercises(session, muscle_group=None)`. Lists use ID order. A missing workout returns `None`. The group filter is exact and case-sensitive; `None` selects all groups and `""` selects the empty group. Reads must not change rows.
