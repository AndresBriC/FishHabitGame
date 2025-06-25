# Fish Habit Game

**TL;DR**: Build positive habits, get cool fish.

---

## What Is This?

This blends habit tracking with a cozy fish-collecting game. Each day:

- New fish appear in your pond.
- You complete habits to earn helpful items.
- You choose when to fish and try catching from the pool.

The better your real-life streaks, the better your chances of landing rare or exotic fish. The vibe is gentle and rewarding missed days mean slower progress, not punishment.

**Inspirations**: Habitica, Animal Crossing, Pokémon, Webfishing, Duolingo.

---

## Daily Game Loop

1. **New Day Begins**
   - Fish pool resets.
   - Habits are reset (unticked).

2. **Complete Habits**
   - Completing a habit grants a random item (e.g., lure, bait).
   - Items boost your chances or reroll the fish pool.

3. **Go Fishing**
   - View daily fish pool.
   - Use items to improve odds (rarity boost, catch chance, etc.).
   - Attempt to catch a fish.
     - If successful, it's added to your inventory and your collection (like a Pokédex).

---

## Tech Stack

- **Backend**: Python
- **Bot Interface**: Discord (`discord.py`)
- **Database**: PostgreSQL
- **DevOps**:
  - GitHub Actions (CI)
  - Pre-commit hooks:
    - `ruff` for Python linting/formatting
    - `sqlfluff` for SQL linting

> Hosting will eventually move to **Azure**.

---

## ERD

![ERD](./Assets/ERD_fishdb.png)

---
