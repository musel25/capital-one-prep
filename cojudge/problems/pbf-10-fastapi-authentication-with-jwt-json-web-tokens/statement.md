# 10. Fastapi authentication with jwt (json web tokens)

[Course list](/?course=pybites-fastapi) · [Original Pybites exercise](https://pybitesplatform.com/bites/fastapi-authentication-with-jwt-json-web-tokens/)

## Required behavior

Complete the supplied OAuth2/JWT functions. POST `/token` accepts form username/password and returns a signed HS256 token with subject and expiry, plus token_type `bearer`. Wrong credentials return 401, detail `Incorrect username or password`. Missing credentials on every food endpoint return 401. Invalid, expired, tampered, missing-subject, or unknown-user tokens return 401, detail `Could not validate credentials`. GET `/` shows only the current user's entries. POST may only create entries for that user (match ID and username); otherwise return 400, detail `Can only add food for current user`. PUT/DELETE of missing entries return 404, detail `Food entry not found`; another user's entry returns 400, detail `Food entry not owned by you`. PUT cannot change ownership. POST cannot overwrite another user's entry ID. Rejected writes preserve existing data. The supplied /create_user endpoint is a classroom fixture. Its fixed signing key is for this exercise only.

## How to solve it

Use Python. Write your solution at the top of the editor. The supplied tests follow it.
Run checks up to three tests. Submit checks all 20 tests.
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
