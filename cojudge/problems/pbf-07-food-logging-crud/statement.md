In this Bite you will use the Pydantic FoodEntry model (which contains the Food and User models as well).
You will create the CRUD (create-read-update-delete) for this model repeating what you've learned in FastAPI Bites 3, 4 and 5.
Here are the endpoints you need to implement with their inputs and responses:
- / [POST] -> receives a FoodEntry, adds it to food_log and returns it.
- /users/{user_id} [GET] -> receives a user_id, filters food_log and returns the foods logged for that user (List[FoodEntry]).
- /{entry_id} [PUT] -> receives an entry_id and new FoodEntry, updates the corresponding entry and returns the new FoodEntry, raises an HTTPException if the entry is not found.
- /{entry_id} [DELETE] -> receives an entry_id and deletes it from food_log, raises an HTTPException if the entry is not found.
We'll hide the previous Food CRUD in the template for now to force the deliberate practice!
Because the platform supports single modules only for exercises, we embedded all three Pydantic models so you might need to scroll down a bit.
Again, we use an in-memory dictionary (food_log: Dict[int, Food]) to focus on the FastAPI / Pydantic (typing) part.
In the SQLModel learning path we'll cover databases and ORMs.
At the end of this Bite you'll have a simple API to track foods. Super exciting!
But it's not very robust yet, so in the next Bite we'll add exception handling.
Then we take a detour to some web development, having you show a user's food log in an HTML template.
In the final Bite we'll lock down the API so only logged-in users can track their own foods.
Note that if you want to code this Bite offline you need to pip install the bcrypt library.

**Constraints:**

- POST returns 201. DELETE returns `{"ok": true}`. A missing update or delete ID returns 404 with detail `Food entry not found`. Preserve insertion order. Tests use matching body and path IDs.
