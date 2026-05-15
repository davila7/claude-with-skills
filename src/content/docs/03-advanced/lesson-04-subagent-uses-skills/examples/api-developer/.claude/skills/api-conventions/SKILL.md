---
title: "api-conventions"
name: api-conventions
description: REST API design conventions for this codebase. Use when writing or reviewing API endpoints, route definitions, response formatting, or client code that calls the API.
user-invocable: false
---

These conventions apply to every API endpoint in this codebase. Follow them exactly. If a new situation requires deviation, document the reason in a code comment.

## URL structure

Pattern: `/api/v{major}/{resource}`

- Resource names are plural nouns in kebab-case: `/api/v1/users`, `/api/v1/billing-accounts`
- Nested resources use path segments: `/api/v1/users/{id}/sessions`
- Do not use verbs in URLs: use `/api/v1/users/{id}` with `DELETE`, not `/api/v1/delete-user/{id}`
- Query parameters are kebab-case: `?page-size=20&sort-by=created-at`

## HTTP methods

| Method | Meaning | Success status |
|--------|---------|----------------|
| GET | Retrieve resource(s), no side effects | 200 |
| POST | Create a new resource | 201 |
| PUT | Replace a resource entirely | 200 |
| PATCH | Partially update a resource | 200 |
| DELETE | Delete a resource | 204 (no body) |

Use GET for all read operations. Do not use POST for reads.

## Response envelope

All successful responses (except 204) use this envelope:

```json
{
  "data": <resource or array of resources>,
  "meta": {
    "timestamp": "<ISO 8601 UTC>",
    "version": "<API minor version string, e.g. 1.4>"
  }
}
```

For list responses, `meta` also includes pagination fields:

```json
{
  "data": [...],
  "meta": {
    "timestamp": "2024-11-01T14:30:00Z",
    "version": "1.4",
    "next_cursor": "<opaque cursor string or null>",
    "limit": 20,
    "count": 20
  }
}
```

`count` is the number of items in the current page, not the total across all pages. Do not include a total count unless explicitly required, as it forces an expensive COUNT query.

## Error format

All error responses use this envelope:

```json
{
  "error": {
    "code": "SNAKE_CASE_ERROR_CODE",
    "message": "Human-readable description safe for end users.",
    "details": {}
  }
}
```

- `code` is a stable machine-readable identifier in SCREAMING_SNAKE_CASE
- `message` is safe for end users — do not include stack traces, SQL, or internal paths
- `details` carries structured field-level information for validation errors:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "One or more fields failed validation.",
    "details": {
      "fields": [
        { "field": "email", "message": "Must be a valid email address." },
        { "field": "birth_date", "message": "Must be in the past." }
      ]
    }
  }
}
```

## Status codes

| Code | Use |
|------|-----|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE (no body) |
| 400 | Malformed request (bad JSON, wrong content-type) |
| 401 | Not authenticated — missing or invalid token |
| 403 | Authenticated but not authorized for this resource |
| 404 | Resource not found |
| 409 | Conflict — resource already exists, optimistic lock conflict |
| 422 | Validation failed — request is well-formed but semantically invalid |
| 429 | Rate limited — include `Retry-After` header |
| 500 | Unexpected server error |
| 503 | Service temporarily unavailable — include `Retry-After` header |

Do not use 400 for validation errors — use 422. Do not use 500 for expected error cases that have a more specific code.

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <token>
```

The token is validated by the auth middleware before the handler runs. Handlers do not validate tokens directly. If the middleware passes, `request.user` (or the framework equivalent) is populated with the authenticated user's identity.

## Pagination

Use cursor-based pagination, not offset-based.

Request parameters:
- `cursor`: opaque cursor string from the previous page's `next_cursor` (absent on first page)
- `limit`: number of items to return, default 20, maximum 100

Response `meta` fields:
- `next_cursor`: cursor to pass for the next page, or `null` if this is the last page
- `limit`: the limit used for this page
- `count`: number of items returned in this page

Do not expose integer offsets or page numbers in the public API.

## Versioning

- Major version in the URL path: `/api/v1/`, `/api/v2/`
- Minor version in the response header: `X-API-Version: 1.4`
- Breaking changes require a new major version
- Additive changes (new fields, new endpoints) increment the minor version
- Deprecated fields are kept for at least two minor versions before removal
