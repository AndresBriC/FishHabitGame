# Fish Habit Game: Contributor Guide

This repository is developed with AI assistance. Treat documents in `docs/` as durable project context. When a code change invalidates documentation, update the relevant document in the same change.

Apply all `AGENTS.md` files governing a modified path. More specific files supplement broader files and take precedence only where their instructions conflict.

## Instruction precedence

Follow instructions in this order:

1. The user’s explicit instructions
2. Applicable `AGENTS.md` files, with more specific files taking precedence over broader files where they conflict
3. Project documentation in `docs/`
4. Existing project conventions

When instructions or documents conflict, identify the conflict rather than resolving it silently.

Use these documents as the primary sources for their areas:

* `docs/product.md`: product goals and intended experience
* `docs/roadmap.md`: current scope and priorities
* `docs/game-rules.md`: authoritative game behavior
* Architecture documentation and ADRs: established technical decisions

## Product and scope

Before changing product behavior or game rules, read `docs/product.md`, `docs/roadmap.md`, and `docs/game-rules.md`.

Work on the current roadmap milestone unless the user explicitly changes priorities.

Do not implement unrelated or out-of-scope ideas opportunistically. Record appropriate ideas in the deferred section of `docs/roadmap.md`. Do not create a new tracking file unless requested.

Do not invent user-visible product behavior, game mechanics, business rules, or requirements that have not been specified. For incidental implementation details, follow existing conventions and choose the smallest reversible option.

## Planning

Before making changes:

* Inspect the relevant implementation, tests, documentation, and ADRs.
* Reuse existing patterns and conventions where appropriate.
* Identify the smallest cohesive change that satisfies the requirement.

A task is non-trivial when it changes behavior, affects multiple modules, modifies an API or schema, or requires a meaningful design decision.

For non-trivial work, explain the proposed approach before making significant architectural or behavioral changes.

## Architecture requirements

These rules are mandatory:

* React renders UI and requests actions. It must not be the source of truth for game rules, catch results, inventory, streaks, or other authoritative game state.
* FastAPI owns authentication, authorization, validation, game rules, and database transactions.
* PostgreSQL is the source of truth for persisted data.
* Every schema change must include a versioned migration.
* Never modify a deployed database schema manually; every schema change must be made through a versioned migration.
* Never rewrite a migration that may already have been applied; create a new migration instead.
* Keep the frontend/backend API contract explicit and typed.
* Update API documentation and affected clients when an endpoint or payload changes.
* The legacy Discord bot is reference-only and must not be included in the new web runtime.
* Do not introduce new frameworks, libraries, or architectural patterns unless explicitly requested or clearly justified and, when material, documented in an ADR.

Preserve the established architecture unless the requested change requires otherwise.

## Implementation and quality

* Prefer the smallest change that satisfies the requirements.
* Keep changes cohesive and reviewable.
* Do not mix unrelated refactoring with feature or bug-fix work.
* Avoid rewriting working code solely for style or preference.
* Prefer explicit, readable code over clever code.
* Reuse existing abstractions before creating new ones.
* Explain significant decisions and non-obvious tradeoffs.
* Do not commit secrets.
* Use environment variables for configuration and keep example configuration files free of real secret values.

## Testing and verification

Add or update tests for behavior changes, especially changes involving fishing attempts, daily resets, streaks, catch persistence, inventory, authentication, or transactions.

Run the smallest test set that adequately covers the change. Run broader checks when changing shared game logic, authentication, migrations, API contracts, or cross-cutting infrastructure.

Before declaring work complete, run the applicable formatter, linter, type checker, and targeted tests.

Do not claim that a check passed unless it was run successfully. When a required check cannot be run or fails for an unrelated reason, report that explicitly.

## Documentation and decisions

Update affected roadmap, product, game-rule, API, architecture, development, or deployment documentation in the same change.

Record durable architecture decisions in `docs/adr/`. Create an ADR for decisions that establish important system boundaries, dependencies, persistence strategies, security approaches, or conventions future contributors must follow. Do not create ADRs for routine implementation details.

## Handling ambiguity

When requirements are ambiguous:

* State the ambiguity.
* Continue with the smallest reasonable assumption when it is safe and easy to reverse.
* Ask for clarification when reasonable interpretations would produce meaningfully different behavior, data models, APIs, or user experiences.
* Do not silently invent missing product behavior.

Document material assumptions in the completion summary.

## Completion report

Before declaring a change complete:

* Summarize the important changes.
* List the checks run and their results.
* Note any applicable checks that were not run and explain why.

When applicable, also:

* Mention material assumptions and tradeoffs.
* Identify anything requiring manual review.
* Note migrations or API contract changes.
* Confirm that affected documentation was updated.
