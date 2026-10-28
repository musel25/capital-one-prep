Great job creating your database tables! Now the gym owner wants to start adding workout programs to the database.
In this exercise, you'll learn how to safely insert data into your database using SQLModel's Session object.

**Constraints:**

- Implement `add_workout(session, name, description="")` and `add_exercise(session, name, muscle_group="")`. Commit, refresh, and return the new row. Duplicate names are allowed. Keep the caller's session open.
- `get_session(engine)` yields a session in a context manager. Closing the generator rolls back uncommitted changes.
