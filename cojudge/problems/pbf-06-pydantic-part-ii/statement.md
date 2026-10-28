# 06. Pydantic part ii

[Course list](/?course=pybites-fastapi) · [Original Pybites exercise](https://pybitesplatform.com/bites/pydantic-part-ii/)

## Required behavior

Define User with `id: int`, `username: str`, and `password: str`. Hash the input password with the supplied helper. Define FoodEntry with `id: int`, `user: User`, `food: Food`, `number_servings: float`, and `date_added: datetime` defaulting to the creation time. Its `total_calories` property multiplies servings by food calories. Preserve explicit dates.

## How to solve it

Use Python. Write your solution at the top of the editor. The supplied tests follow it.
Run checks up to three tests. Submit checks all 6 tests.
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
