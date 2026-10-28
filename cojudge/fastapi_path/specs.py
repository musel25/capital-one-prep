"""Reference solutions and explicit contracts for the imported FastAPI path."""

CONTRACTS = [
    'Create `app = FastAPI()`. GET `/` returns the welcome message shown in the tests. POST `/` returns 405.',
    'Define `Food(BaseModel)` with required `id: int`, `name: str`, `serving_size: str`, `kcal_per_serving: int`, and `protein_grams: float`. Set `fibre_grams: float = 0`. Use normal Pydantic 2 coercion and validation.',
    'POST `/` receives a Food, stores it in `foods` by ID, and returns it with status 201. Keep the other items. Missing required fields return 422. Duplicate-ID handling is deferred to a later exercise.',
    'Keep the supplied create endpoint. GET `/` returns a list of all Foods in insertion order. GET `/{food_id}` returns that Food. For this early exercise, a missing ID raises KeyError; the supplied tests expect this. Later exercises teach HTTP errors.',
    'Keep the supplied create/read endpoints. PUT `/{food_id}` replaces an existing Food and returns it. DELETE `/{food_id}` removes it and returns `{"ok": true}`. A missing ID in either write returns 404 with detail `Food not found`. Tests use matching body and path IDs.',
    'Define User with `id: int`, `username: str`, and `password: str`. Hash the input password with the supplied helper. Define FoodEntry with `id: int`, `user: User`, `food: Food`, `number_servings: float`, and `date_added: datetime` defaulting to the creation time. Its `total_calories` property multiplies servings by food calories. Preserve explicit dates.',
    'POST `/` creates a FoodEntry with status 201 in `food_log`. GET `/users/{user_id}` returns only that user\'s entries in insertion order. PUT `/{entry_id}` replaces an existing entry. DELETE removes it and returns `{"ok": true}`. Missing update/delete IDs return 404 with detail `Food entry not found`. Tests use matching body and path IDs.',
    'Extend the supplied POST endpoint. Reject a duplicate entry ID with 400 and detail `Food entry already logged, use an update request`. Sum calories for the incoming user ID only. Reject a total above `user.max_daily_calories` with 400 and detail `Cannot add more food than daily caloric allowance = {limit} kcal / day`. Equality is allowed. Failed writes must preserve the dictionary. Assume all entries belong to the same day. The default limit is 2250.',
    'Keep the supplied create endpoint. GET `/{username}` returns an HTMLResponse with status 200. Use HTML_TEMPLATE and TABLE_ROW to show that user\'s entries in insertion order. Include the food name, date, servings and serving size, and total calories. Escape text fields before insertion. An unknown username gets an empty table.',
    'Complete the supplied OAuth2/JWT functions. POST `/token` accepts form username/password and returns a signed HS256 token with subject and expiry, plus token_type `bearer`. Wrong credentials return 401, detail `Incorrect username or password`. Missing credentials on every food endpoint return 401. Invalid, expired, tampered, missing-subject, or unknown-user tokens return 401, detail `Could not validate credentials`. GET `/` shows only the current user\'s entries. POST may only create entries for that user (match ID and username); otherwise return 400, detail `Can only add food for current user`. PUT/DELETE of missing entries return 404, detail `Food entry not found`; another user\'s entry returns 400, detail `Food entry not owned by you`. PUT cannot change ownership. POST cannot overwrite another user\'s entry ID. Rejected writes preserve existing data. The supplied /create_user endpoint is a classroom fixture. Its fixed signing key is for this exercise only.',
]

ADDITIONS = {
1: '''
@app.get("/")
async def root():
    return {"message": "Welcome to PyBites' FastAPI Learning Path 🐍 🎉"}
''',
2: '''
class Food(BaseModel):
    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: float = 0
''',
3: '''
@app.post("/", status_code=201)
async def create_food(food: Food):
    foods[food.id] = food
    return food
''',
4: '''
from typing import List

@app.get("/", response_model=List[Food])
async def read_foods():
    return list(foods.values())

@app.get("/{food_id}", response_model=Food)
async def read_food(food_id: int):
    return foods[food_id]
''',
5: '''
@app.put("/{food_id}", response_model=Food)
async def update_food(food_id: int, food: Food):
    if food_id not in foods:
        raise HTTPException(status_code=404, detail="Food not found")
    foods[food_id] = food
    return food

@app.delete("/{food_id}")
async def delete_food(food_id: int):
    if food_id not in foods:
        raise HTTPException(status_code=404, detail="Food not found")
    del foods[food_id]
    return {"ok": True}
''',
6: '''
from pydantic import Field

class User(BaseModel):
    id: int
    username: str
    password: str

    def __init__(self, **data: Any):
        if "password" in data:
            data["password"] = get_password_hash(data["password"])
        super().__init__(**data)

class FoodEntry(BaseModel):
    id: int
    user: User
    food: Food
    date_added: datetime = Field(default_factory=datetime.now)
    number_servings: float

    @property
    def total_calories(self):
        return self.food.kcal_per_serving * self.number_servings
''',
7: '''
from fastapi import HTTPException

@app.post("/", status_code=201)
async def create_food_entry(entry: FoodEntry):
    food_log[entry.id] = entry
    return entry

@app.get("/users/{user_id}", response_model=List[FoodEntry])
async def get_foods_for_user(user_id: int):
    return [entry for entry in food_log.values() if entry.user.id == user_id]

@app.put("/{entry_id}", response_model=FoodEntry)
async def update_food_entry(entry_id: int, new_entry: FoodEntry):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")
    food_log[entry_id] = new_entry
    return new_entry

@app.delete("/{entry_id}")
async def delete_food_entry(entry_id: int):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")
    del food_log[entry_id]
    return {"ok": True}
''',
}

ERROR_CHECKS = '''
    if entry.id in food_log:
        raise HTTPException(status_code=400, detail="Food entry already logged, use an update request")
    consumed = sum(item.total_calories for item in food_log.values() if item.user.id == entry.user.id)
    if consumed + entry.total_calories > entry.user.max_daily_calories:
        raise HTTPException(status_code=400, detail=(
            f"Cannot add more food than daily caloric allowance = {entry.user.max_daily_calories} kcal / day"))
'''

HTML_BODY = '''
    from html import escape
    rows = []
    for entry in food_log.values():
        if entry.user.username == username:
            rows.append(TABLE_ROW.format(
                food_name=escape(entry.food.name), date_added=entry.date_added,
                number_servings=entry.number_servings,
                serving_size=escape(entry.food.serving_size), total_calories=entry.total_calories))
    return HTMLResponse(content=HTML_TEMPLATE.format(username=escape(username), table_rows="".join(rows)))
'''

AUTH = '''
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    from datetime import timezone
    claims = data.copy()
    claims["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    error = HTTPException(status_code=401, detail="Could not validate credentials",
                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise error
    except JWTError:
        raise error
    user = get_user(username)
    if user is None:
        raise error
    return user

@app.post("/create_user", status_code=201)
async def create_user(user: User):
    users_db[user.username] = user
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/", status_code=201)
async def create_food_entry(entry: FoodEntry, current_user: User = Depends(get_current_user)):
    if entry.user.id != current_user.id or entry.user.username != current_user.username:
        raise HTTPException(status_code=400, detail="Can only add food for current user")
    if entry.id in food_log and food_log[entry.id].user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Food entry not owned by you")
    food_log[entry.id] = entry
    return entry

@app.get("/", response_model=List[FoodEntry])
async def get_foods_for_user(current_user: User = Depends(get_current_user)):
    return [entry for entry in food_log.values() if entry.user.id == current_user.id]

@app.put("/{entry_id}", response_model=FoodEntry)
async def update_food_entry(entry_id: int, new_entry: FoodEntry, current_user: User = Depends(get_current_user)):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")
    if (food_log[entry_id].user.id != current_user.id or new_entry.user.id != current_user.id
            or new_entry.user.username != current_user.username):
        raise HTTPException(status_code=400, detail="Food entry not owned by you")
    food_log[entry_id] = new_entry
    return new_entry

@app.delete("/{entry_id}")
async def delete_food_entry(entry_id: int, current_user: User = Depends(get_current_user)):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")
    if food_log[entry_id].user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Food entry not owned by you")
    del food_log[entry_id]
    return {"ok": True}
'''

# Each fault must fail at least one actual exercise test.
MUTATIONS = {
1: [('wrong welcome', "Welcome to PyBites' FastAPI Learning Path 🐍 🎉", 'hello')],
2: [('wrong default', 'fibre_grams: float = 0', 'fibre_grams: float = 1')],
3: [('wrong status', 'status_code=201', 'status_code=200')],
4: [('drops foods', 'return list(foods.values())', 'return []')],
5: [('delete keeps item', 'del foods[food_id]', 'pass')],
6: [('wrong calories', 'self.food.kcal_per_serving * self.number_servings', 'self.food.kcal_per_serving')],
7: [('leaks other users', 'if entry.user.id == user_id', 'if True')],
8: [('allows duplicates', 'if entry.id in food_log:', 'if False:')],
9: [('leaks other users', 'if entry.user.username == username:', 'if True:')],
10: [('ignores password', 'not verify_password(password, user.password)', 'False'),
     ('allows expired tokens', 'algorithms=[ALGORITHM])', 'algorithms=[ALGORITHM], options={"verify_exp": False})'),
     ('allows owner change', 'or new_entry.user.id != current_user.id', 'or False')],
}
