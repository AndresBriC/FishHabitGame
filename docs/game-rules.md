# Game rules

This document is the source of truth for game behavior. Values may change during balancing, but the backend and tests must change with this document.

## Initial vertical slice

- Each registered player has a personal daily pond.
- A daily pond contains three fish entries.
- A player starts each day with five fishing attempts.
- An uncaught, unexpired pond entry may be selected for one catch attempt.
- A catch roll uses that fish type's base catch rate.
- Each catch attempt consumes one attempt, whether it succeeds or fails.
- A successful catch creates one collection record and marks that pond entry caught.
- A pond entry cannot be caught more than once.
- A player cannot catch an entry from another player's pond.
- The daily pond and attempts reset at 00:00 UTC.

## Initial spawn distribution

| Rarity | Probability |
| --- | ---: |
| Common | 60% |
| Uncommon | 25% |
| Rare | 12.5% |
| Exotic | 2.5% |

## Deferred rules

Habit rewards, streak effects, items, rods, rerolls, and size variation are not part of the first vertical slice.
