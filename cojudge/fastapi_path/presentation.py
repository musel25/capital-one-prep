"""Original task text and concrete examples for the FastAPI path."""
import re


STARTS = {
    1: 'Welcome to this FastAPI learning path.',
    2: 'Pydantic is an awesome library',
    3: 'Now with the Pydantic Food model',
    4: 'Now that our API can add food objects',
    5: "Now that we're able to create",
    6: 'In order to measure daily food intake',
    7: 'In this Bite you will use the Pydantic FoodEntry',
    8: "In this Bite we'll take the API",
    9: 'You use FastAPI primarily to build APIs',
    10: 'Up to this point anyone can modify',
}


def original_description(spec):
    text = spec['page']['desc'].split(STARTS[spec['number']], 1)[1]
    text = STARTS[spec['number']] + text
    text = re.split(r'\n\s+(?:app|models)\s+\n', text, maxsplit=1)[0].strip()
    text = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', text)
    text = text.replace('Bearer <redacted>', 'Bearer `<redacted>`')
    if spec['number'] == 2:
        start = text.index('Attribute\n')
        end = text.index('* kcal = calories')
        text = text[:start] + ('| Attribute | Type | Example |\n| --- | --- | --- |\n'
            '| id | int | 1 |\n| name | str | oatmeal |\n| serving_size | str | 100 grams |\n'
            '| kcal_per_serving | int | 336 |\n| protein_grams | float | 13.2 |\n'
            '| fibre_grams | float | 10.1 |\n\n') + text[end:]
    if spec['number'] == 6:
        text = re.sub(r'(?<=\S)- (?=\w+ ->)', '\n- ', text)
    if spec['number'] == 9:
        start = text.index('Food\nAdded\n')
        end = text.index('We provided the show_foods_for_user')
        text = text[:start] + ('| Food | Added | Servings | Calories (kcal) |\n| --- | --- | --- | --- |\n'
            '| egg | 2022-03-13 11:02:37.500968 | 1.5 x piece | 117.0 |\n'
            '| oatmeal | 2022-03-13 11:02:37.500968 | 2.0 x 100 grams | 672.0 |\n\n') + text[end:]
        text = text.replace('<html lang="en">', '\n```html\n<html lang="en">').replace('</html>', '</html>\n```\n')
    return text


CLARIFICATIONS = {
    1: (),
    2: ('Use Pydantic 2 validation and type conversion.',),
    3: ('Use POST `/`. Let FastAPI validate the request body.',),
    4: ('Use GET `/` and GET `/{food_id}`. Return all foods in insertion order. A missing ID raises `KeyError` in this exercise.',),
    5: ('Use PUT and DELETE `/{food_id}`. Tests use matching body and path IDs.',),
    6: ('Create a fresh default timestamp for each entry. Keep an explicit timestamp when supplied.',),
    7: ('POST returns 201. DELETE returns `{"ok": true}`. A missing update or delete ID returns 404 with detail `Food entry not found`. Preserve insertion order. Tests use matching body and path IDs.',),
    8: ('Count calories for the incoming user ID only. Equality with the limit is allowed. A rejected request must not change `food_log`.',),
    9: ('Use GET `/{username}`. Preserve insertion order. Escape text fields in HTML. An unknown username gets an empty table.',),
    10: ('Use the supplied function signatures. POST `/token` accepts form credentials and returns an HS256 token with subject and expiry, plus `token_type="bearer"`. Wrong credentials return 401 with detail `Incorrect username or password`. Invalid or missing food-endpoint credentials return 401; invalid tokens use detail `Could not validate credentials`.',
         'GET `/` returns only the current user\'s entries. POST must match that user\'s ID and username; otherwise return 400 with detail `Can only add food for current user`. PUT cannot change ownership. POST cannot overwrite another user\'s entry ID.',
         'PUT and DELETE return 404 with detail `Food entry not found` for a missing entry. For another user\'s entry, return 400 with detail `Food entry not owned by you`. Rejected writes must preserve existing entries.'),
}


CLIENT = 'from fastapi.testclient import TestClient\nclient = TestClient(app)\n'
FOOD = '{"id": 1, "name": "egg", "serving_size": "piece", "kcal_per_serving": 78, "protein_grams": 6.3}'

# Every input is runnable after the exercise implementation. Outputs are stdout.
EXAMPLES = {
    1: [(CLIENT + 'response = client.get("/")\nprint(response.status_code)\nprint(response.json())',
         '200\n{\'message\': "Welcome to PyBites\' FastAPI Learning Path 🐍 🎉"}')],
    2: [('food = Food(**' + FOOD + ')\nprint(food.name, food.fibre_grams)', 'egg 0')],
    3: [(CLIENT + 'foods.clear()\nresponse = client.post("/", json=' + FOOD + ')\nprint(response.status_code)\nprint(response.json())',
         "201\n{'id': 1, 'name': 'egg', 'serving_size': 'piece', 'kcal_per_serving': 78, 'protein_grams': 6.3, 'fibre_grams': 0.0}")],
    4: [(CLIENT + 'foods.clear()\nclient.post("/", json=' + FOOD + ')\nprint(client.get("/1").json()["name"])\nprint(len(client.get("/").json()))', 'egg\n1')],
    5: [(CLIENT + 'foods.clear()\nclient.post("/", json=' + FOOD + ')\nresponse = client.delete("/1")\nprint(response.status_code, response.json())\nprint(client.delete("/1").status_code)', "200 {'ok': True}\n404")],
    6: [('user = User(id=1, username="Ada", password="test-password")\nfood = Food(**' + FOOD + ')\nentry = FoodEntry(id=1, user=user, food=food, number_servings=1.5)\nprint(entry.total_calories)', '117.0')],
    7: [(CLIENT + 'food_log.clear()\nprint(client.get("/users/42").json())\nresponse = client.delete("/999")\nprint(response.status_code, response.json())', "[]\n404 {'detail': 'Food entry not found'}")],
    8: [(CLIENT + 'food_log.clear()\nentry = {"id": 1, "user": {"id": 1, "username": "Ada", "password": "test-password"}, "food": ' + FOOD + ', "number_servings": 1}\nprint(client.post("/", json=entry).status_code)\nresponse = client.post("/", json=entry)\nprint(response.status_code, response.json())',
         "201\n400 {'detail': 'Food entry already logged, use an update request'}")],
    9: [(CLIENT + 'from bs4 import BeautifulSoup\nfood_log.clear()\nresponse = client.get("/Ada")\nsoup = BeautifulSoup(response.text, "html.parser")\nprint(response.status_code)\nprint(soup.title.text)\nprint([cell.text for cell in soup.find_all("th")])\nprint(len(soup.find("tbody").find_all("tr")))',
         "200\nFood log for Ada\n['Food', 'Added', 'Servings', 'Calories (kcal)']\n0")],
    10: [(CLIENT + 'response = client.post("/token", data={"username": "missing-user", "password": "wrong"})\nprint(response.status_code, response.json())\nprint(client.get("/").status_code)',
          "401 {'detail': 'Incorrect username or password'}\n401")],
}
