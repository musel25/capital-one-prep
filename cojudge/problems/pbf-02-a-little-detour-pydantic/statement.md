# 02. A little detour: pydantic

[Course list](/?course=pybites-fastapi) · [Original Pybites exercise](https://pybitesplatform.com/bites/a-little-detour-pydantic/)

## Required behavior

Define `Food(BaseModel)` with required `id: int`, `name: str`, `serving_size: str`, `kcal_per_serving: int`, and `protein_grams: float`. Set `fibre_grams: float = 0`. Use normal Pydantic 2 coercion and validation.

## How to solve it

Use Python. Write your solution at the top of the editor. The supplied tests follow it.
Run checks up to three tests. Submit checks all 5 tests.
Each check runs real pytest and FastAPI in a fresh process. No server or network is needed.
Keep the supplied tests and adapter unchanged. Failures show the pytest test name and error.

## Source and changes

The starter and tests were imported from the exercise pages accessible in the user's Pybites session.
Example password fields and the classroom signing key were restored with explicit test values after export redaction.
FoodEntry uses a per-instance timestamp default. Tests labelled `test_added_` are added Cojudge checks.
The required behavior above summarizes the source description and states the added checks.
The reference solution was written for this course.

The runtime uses Python 3.11, FastAPI 0.161.1, Pydantic 2, real pytest,
HTTPX, Passlib/bcrypt, python-jose, python-multipart, and BeautifulSoup.
Package versions are locked in `cojudge/fastapi_path/uv.lock` in the content repository.

For an old saved solution, use **+** beside the editor tabs to open the current starter.
Copy your code into that tab. Keep your old saved tab.
