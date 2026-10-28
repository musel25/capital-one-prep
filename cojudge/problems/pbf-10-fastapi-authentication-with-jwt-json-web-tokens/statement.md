Up to this point anyone can modify food entries in the food log API, for any user!
That is not desired and in this Bite we will have you lock down the API.
You'll work through the OAuth2 with Password (and hashing), Bearer `<redacted>` JWT tokens guide adding all the pieces to effectively make the API secure using using JWT tokens and secure password hashing. You'll use FastAPI's elegant Depends() to lock down the endpoints that were copied over from a previous Bite.
Good luck!
This Bite concludes the FastAPI learning path. Stay tuned for an SQLModel learning path where we build a similar API but using an ORM / database for persistence.
If you have any feedback on this learning path use the feedback form upon completing any of the Bites.

**Constraints:**

- Use the supplied function signatures. POST `/token` accepts form credentials and returns an HS256 token with subject and expiry, plus `token_type="bearer"`. Wrong credentials return 401 with detail `Incorrect username or password`. Invalid or missing food-endpoint credentials return 401; invalid tokens use detail `Could not validate credentials`.
- GET `/` returns only the current user's entries. POST must match that user's ID and username; otherwise return 400 with detail `Can only add food for current user`. PUT cannot change ownership. POST cannot overwrite another user's entry ID.
- PUT and DELETE return 404 with detail `Food entry not found` for a missing entry. For another user's entry, return 400 with detail `Food entry not owned by you`. Rejected writes must preserve existing entries.
