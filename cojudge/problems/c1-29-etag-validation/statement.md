# 29. Validate cached representations with ETags

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 30 minutes**

**Before this problem:** Problems 21–24; request contracts and versioned state.

## Learn first

A cached response can carry a validator called an entity tag, or ETag. The client later sends that tag with a conditional read. If it still matches, the server can return a not-modified response without the representation body. The client then keeps its cached body. For If-None-Match on GET, weak tags can match the same underlying tag value. A write can change the current validator. This exercise uses an integer version to create simple tags and supplies an already parsed list of client tags. It covers validation, not cache freshness, expiration, header parsing, or a complete HTTP cache implementation.

## Your task

`initial` is `{version:positive_int, body:string}`. Requests are `{op:"put", body:string}` or `{op:"get", tags:null|[tag,...]}`. The current strong ETag is the string `"vN"`, including its quote characters, where N is the version. Every put increments version by one, even for an unchanged body, and returns `{status:200, etag:current_tag, body:current_body}`. A get has no validator when tags is null. A supplied tag matches if it is `*`, the current strong tag, or `W/` followed by that strong tag. Any match returns `{status:304, etag:current_tag, body:null}`. Otherwise return status 200 with the body. Return responses in request order. The resource always exists. No actual header parser or network is required.

## Examples

### Example 1: unconditional read returns representation

Input to `solve`:
```json
{
  "initial": {
    "version": 1,
    "body": "hello"
  },
  "requests": [
    {
      "op": "get",
      "tags": null
    }
  ]
}
```
Return:
```json
[
  {
    "status": 200,
    "etag": "\"v1\"",
    "body": "hello"
  }
]
```

### Example 2: matching tag avoids body

Input to `solve`:
```json
{
  "initial": {
    "version": 1,
    "body": "hello"
  },
  "requests": [
    {
      "op": "get",
      "tags": [
        "\"v1\""
      ]
    }
  ]
}
```
Return:
```json
[
  {
    "status": 304,
    "etag": "\"v1\"",
    "body": null
  }
]
```

### Example 3: write invalidates old validator

Input to `solve`:
```json
{
  "initial": {
    "version": 1,
    "body": "hello"
  },
  "requests": [
    {
      "op": "put",
      "body": "new"
    },
    {
      "op": "get",
      "tags": [
        "\"v1\""
      ]
    }
  ]
}
```
Return:
```json
[
  {
    "status": 200,
    "etag": "\"v2\"",
    "body": "new"
  },
  {
    "status": 200,
    "etag": "\"v2\"",
    "body": "new"
  }
]
```

## Constraints

- 0–200 requests; initial version is 1–1000000. Bodies are ASCII strings of length 0–200.
- A tags list has 0–20 entries. Each is *, a quoted vN tag, or W/ followed by a quoted vN tag; N is 1–1000000.
- Tags are pre-parsed; malformed tags and cache expiration are outside the domain.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 29 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-none-match)
- [Official documentation 2](https://www.rfc-editor.org/rfc/rfc9111.html)
