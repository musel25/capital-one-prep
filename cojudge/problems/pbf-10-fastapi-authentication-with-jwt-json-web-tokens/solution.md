## Reference solution

```python
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

# normally would load from env
SECRET_KEY = (
    "classroom-only-signing-key-do-not-use-in-production"  # noqa S105
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class Food(BaseModel):
    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: float = 0


class User(BaseModel):
    id: int
    username: str
    password: str

    def __init__(self, **data: Any):
        data["password"] = get_password_hash(data["password"])
        super().__init__(**data)


class FoodEntry(BaseModel):
    id: int
    user: User
    food: Food
    date_added: datetime = Field(default_factory=datetime.now)
    number_servings: float


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
food_log: Dict[int, FoodEntry] = {}

# We created an extra in memory user DB
users_db: Dict[str, User] = {}


def verify_password(plain_password, hashed_password):
    """Provided, all good"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Provided, all good"""
    return pwd_context.hash(password)


def get_user(username: str):
    """Provided, all good"""
    if username in users_db:
        user = users_db[username]
        return user



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
```
