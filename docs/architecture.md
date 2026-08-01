# Architecture

## System boundary

```text
Browser (React + TypeScript)
        | JSON over HTTPS
FastAPI backend
        | SQLAlchemy transactions and migrations
PostgreSQL
```

## Responsibilities

### React frontend

- Renders responsive screens and feedback.
- Stores only temporary interface state.
- Requests data and actions from the API.
- Never determines a catch result or changes game data directly.

### FastAPI backend

- Authenticates players.
- Validates requests and returns typed responses.
- Owns game rules and time-based behavior.
- Executes database writes atomically.

### PostgreSQL

- Persists users, fish types, daily pond entries, catches, habits, items, and rewards.
- Is changed only through versioned migrations.

## First API surface

- `POST /auth/register`
- `POST /auth/login`
- `GET /me`
- `GET /pond/today`
- `POST /pond/{pond_entry_id}/catch`
- `GET /collection`

## Guiding constraints

- The API is the only boundary through which the web client changes player data.
- Catching must be one transaction: validate pond entry and attempt, roll outcome, persist the result, and decrement the attempt.
- All dates and reset calculations are stored and evaluated consistently in UTC.
