Now with the Pydantic Food model defined we can start creating objects through FastAPI - exciting!
In this Bite you will make a create_food() endpoint that receives a Food object payload and adds the food to a dictionary. We use an in memory data structure to keep things simple for starters.
The endpoint should return the created Food object as JSON and a 201 Created status upon success.
The global foods dictionary will use food IDs (int) as keys and Food objects as values.
After creating a food object, the foods dictionary will look like this:
{1: Food(id=1, name='egg', serving_size='piece', kcal_per_serving=78, protein_grams=6.3, fibre_grams=0)}
We know that using a global object isn't ideal, but we want to separate FastAPI from SQLModel to teach this gradually.
This Bite only covers the happy path. We'll handle errors (like duplicates or invalid payloads) in a later Bite.
So go ahead and write the endpoint, and check the tests to see how we validate the code. Have fun!

**Constraints:**

- Use POST `/`. Let FastAPI validate the request body.
