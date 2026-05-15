---
title: "team-api-conventions"
name: team-api-conventions
description: API design conventions for this codebase. Use whenever writing or reviewing API endpoints, route handlers, or HTTP clients.
user-invocable: false
---

## Team API conventions

Apply these conventions whenever you write, review, or modify API endpoints, route handlers, request validation, or HTTP client code in this codebase.

### REST naming

- Use lowercase, hyphen-separated resource names in URLs: `/user-profiles`, not `/userProfiles` or `/user_profiles`.
- Resources are plural nouns: `/invoices`, `/line-items`, not `/invoice`, `/lineItem`.
- Nested resources express ownership: `/invoices/{id}/line-items`.
- Actions that do not map cleanly to CRUD use a verb suffix on the resource: `/invoices/{id}/send`, `/invoices/{id}/void`.
- Query parameters are camelCase: `?pageSize=20&startAfter=abc`.

### Response format

All API responses use a consistent envelope:

```json
{
  "data": {},
  "meta": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

List responses add `pagination` to `meta`:

```json
{
  "data": [],
  "meta": {
    "requestId": "uuid",
    "timestamp": "ISO-8601",
    "pagination": {
      "total": 142,
      "pageSize": 20,
      "nextCursor": "opaque-string-or-null"
    }
  }
}
```

Do not return bare arrays or bare objects at the top level.

### Error format

```json
{
  "error": {
    "code": "INVOICE_NOT_FOUND",
    "message": "No invoice with id 'xyz' exists.",
    "requestId": "uuid"
  }
}
```

- `code` is SCREAMING_SNAKE_CASE and stable across releases. Client code switches on this value.
- `message` is human-readable and may change between releases.
- HTTP status codes: 400 for client errors, 401 for unauthenticated, 403 for unauthorized, 404 for not found, 409 for conflicts, 422 for validation failures, 500 for server errors. Do not use 200 with an error body.

### Versioning

- Version in the URL path: `/v1/invoices`, `/v2/invoices`.
- Never version individual endpoints separately. When a breaking change is needed, version the entire API surface together.
- Maintain at least one prior major version for six months after a new version is released.

### Authentication

- All authenticated requests use the header `Authorization: Bearer <token>`.
- Never accept tokens as query parameters. Log warnings if a query parameter token is detected (it may have been sent by an older client).
- Service-to-service calls use `X-Service-Token` instead of `Authorization` and are validated differently at the gateway.

### When reviewing API code

Flag any of the following as review comments:
- Bare array or bare object response bodies
- Missing `requestId` in responses
- Error bodies that return 200 OK
- Tokens accepted via query parameters
- Inconsistent resource naming (mixed plural/singular, mixed casing)
