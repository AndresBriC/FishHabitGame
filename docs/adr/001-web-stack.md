# ADR 001: Use FastAPI and React for the web application

**Status:** Accepted
**Date:** 2026-08-01

## Context

The original MVP used a Discord bot. The product now needs a visual, mobile-friendly interface for habits, a daily pond, and a fish collection while retaining Python and PostgreSQL.

## Decision

Use FastAPI for the backend API and React with TypeScript and Vite for the browser client. PostgreSQL remains the persistent datastore. The Discord bot is not part of the new application runtime.

## Consequences

- Game rules and trusted writes live in the FastAPI service.
- React is independently deployable and communicates with FastAPI through a typed JSON API.
- The project gains frontend tooling and a clear API boundary.
- A future native or game-engine client can reuse the backend API.

## Alternatives considered

- Continue with Discord: fast but unsuitable for a visual collection and habit interface.
- Server-rendered templates with HTMX: simpler initial delivery, but less suitable for the intended rich interface.
- Godot as the primary client: strong game interaction but disproportionate complexity for habits and account screens.
