Welcome to the SQLModel learning path! You're about to build a workout tracking app for a local gym.
The gym owner wants to digitize their workout programs and exercises. Your first task? Create the database schema to store workouts (like "Upper Body Day" or "Leg Day") and exercises (like "Bench Press" or "Squats").

**Constraints:**

- Define `Workout` and `Exercise` tables with optional integer primary key `id=None` and required string `name`. Default `Workout.description` and `Exercise.muscle_group` to `""`. `create_tables(engine)` must preserve rows when called again.
