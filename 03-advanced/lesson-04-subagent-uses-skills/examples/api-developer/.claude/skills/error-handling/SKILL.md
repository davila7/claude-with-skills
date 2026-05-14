---
name: error-handling
description: Error handling patterns for API endpoints. Use when implementing error handling, writing middleware, or reviewing how errors are caught and formatted in API code.
user-invocable: false
---

These patterns apply to all API endpoint handlers in this codebase. Every error must be handled explicitly — no unhandled exceptions may reach the HTTP framework.

## Fundamental rule

All errors are caught and formatted at the handler level (or in a central error-handling middleware/decorator that wraps every handler). The framework never renders an unhandled exception as a response.

## Central error handling

Use the shared error-handling decorator or middleware for every handler. Do not write try/catch blocks that format HTTP responses directly inside business logic. The pattern:

```
request → auth middleware → handler → error middleware → formatted response
```

If the handler throws, the error middleware intercepts it, logs it if appropriate, and converts it to the standard error envelope before sending the response.

## Logging rules

Log 5xx errors (unexpected server errors) at the ERROR level with:
- Request ID (from the `X-Request-ID` header, or generate one if absent)
- Error message
- Full stack trace
- Request method and path (not the full URL — avoid logging query parameters that may contain tokens)

Do not log 4xx errors at ERROR level. Log them at DEBUG level if useful for debugging, but 4xx errors are expected client behavior and should not generate noise in error monitoring.

Never log request bodies or response bodies unless explicitly enabled for debugging in a non-production environment.

## What belongs in API responses

Never include in an API error response:
- Stack traces
- SQL queries or database error messages
- Internal file paths
- Environment variable names or values
- Dependency version strings

Always include:
- A stable `code` in SCREAMING_SNAKE_CASE
- A human-readable `message` safe for end users

## Mapping error types to status codes

### Input validation errors → 422

Use 422 when the request is syntactically valid but semantically invalid (missing required fields, wrong value format, business rule violation detectable before touching external state).

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "One or more fields failed validation.",
    "details": {
      "fields": [
        { "field": "email", "message": "Must be a valid email address." }
      ]
    }
  }
}
```

### Authentication errors → 401

Use 401 when the request has no token, the token is expired, or the token is invalid. The message should not indicate which of these conditions applies — treat them identically to avoid enumeration attacks.

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication is required to access this resource."
  }
}
```

### Authorization errors → 403

Use 403 when the user is authenticated but does not have permission to perform the action. Use a consistent message that does not reveal whether the resource exists.

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to perform this action."
  }
}
```

### Resource not found → 404

Use 404 when a resource addressed by ID does not exist or has been deleted. If the user does not have permission to know whether the resource exists, return 403 instead of 404.

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "The requested resource was not found."
  }
}
```

### Database constraint violations → 409 or 422

- Unique constraint violation (e.g., email already taken) → 409 Conflict
- Foreign key violation that reveals a missing parent resource → 422 Validation Failed
- Do not let raw database error messages propagate — catch them in the data layer and convert them before they reach the handler

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "A user with this email address already exists."
  }
}
```

### Timeouts → 503

Use 503 when a downstream dependency (database, external API) times out. Include a `Retry-After` header with a suggested retry delay in seconds.

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "The service is temporarily unavailable. Please try again shortly."
  }
}
```

Response header: `Retry-After: 30`

### Rate limiting → 429

Use 429 when the client has exceeded the rate limit. Include `Retry-After` and `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please slow down."
  }
}
```

### Unknown errors → 500

All other unhandled exceptions become 500. The response body contains only a generic message. The real error is logged internally.

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. If this persists, contact support."
  }
}
```

An internal alert must fire for every 500 response in production. Do not let 500 errors go undetected.

## Error codes reference

| Code | Status | Meaning |
|------|--------|---------|
| `VALIDATION_FAILED` | 422 | One or more input fields failed validation |
| `UNAUTHENTICATED` | 401 | Missing or invalid authentication token |
| `FORBIDDEN` | 403 | Authenticated but not authorized |
| `NOT_FOUND` | 404 | Resource does not exist |
| `CONFLICT` | 409 | Resource already exists or state conflict |
| `RATE_LIMITED` | 429 | Client exceeded rate limit |
| `SERVICE_UNAVAILABLE` | 503 | Downstream timeout or unavailability |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

Use these codes consistently. Do not create one-off codes for situations already covered here.
