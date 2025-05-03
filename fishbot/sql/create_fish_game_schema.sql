CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,  -- Discord user ID
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fishing_attempts_left INTEGER DEFAULT 5,  -- Daily fishing limit
    fishing_attempts_reset_at TIMESTAMP,  -- When attempts will refresh
    current_rod_id INTEGER  -- Reference to equipped rod
);

-- List of fish types
CREATE TABLE fish_types (
    fish_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    rarity VARCHAR(50) NOT NULL,  -- common, uncommon, rare, legendary
    base_catch_rate DECIMAL(3, 2) NOT NULL,  -- Percentage chance of catching
    min_size DECIMAL(6, 2),  -- For size variation
    max_size DECIMAL(6, 2),
    image_url VARCHAR(255),  -- Optional image reference
    ecosystem VARCHAR(50) DEFAULT 'pond'  -- For future ecosystem expansion
);


-- Caught fish
CREATE TABLE user_fish (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users (user_id),
    fish_id INTEGER NOT NULL REFERENCES fish_types (fish_id),
    caught_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    size DECIMAL(6, 2) NOT NULL  -- Actual size of this specific catch
);

-- List of item types
CREATE TABLE item_types (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    item_type VARCHAR(50) NOT NULL,  -- consumable, permanent
    effect_type VARCHAR(50) NOT NULL,  -- catch_rate_boost, reroll, lure, etc.
    effect_value DECIMAL(5, 2),  -- Percentage or numeric effect value
    effect_duration INTEGER,  -- For consumables, how many uses before expiry
    rarity VARCHAR(50) NOT NULL  -- common, uncommon, rare, legendary
);

-- Items held by users
CREATE TABLE user_items (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users (user_id),
    item_id INTEGER NOT NULL REFERENCES item_types (item_id),
    quantity INTEGER NOT NULL DEFAULT 1
);

-- Holds the fish spawned in the pond for each day
CREATE TABLE daily_pond (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users (user_id),
    fish_id INTEGER NOT NULL REFERENCES fish_types (fish_id),
    spawned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,  -- When this fish despawns (daily reset)
    caught BOOLEAN DEFAULT FALSE  -- Whether user has caught this spawn
);

CREATE TABLE habits (
    habit_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users (user_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    frequency INTEGER DEFAULT 1,  -- Days between required completions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE habit_completions (
    id SERIAL PRIMARY KEY,
    habit_id INTEGER NOT NULL REFERENCES habits (habit_id),
    user_id VARCHAR(255) NOT NULL REFERENCES users (user_id),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE habit_streaks (
    streak_id SERIAL PRIMARY KEY,
    habit_id INTEGER NOT NULL REFERENCES habits (habit_id),
    user_id VARCHAR(255) NOT NULL REFERENCES users (user_id),
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_completion_date DATE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the current started
);

CREATE TABLE streak_rewards (
    reward_id SERIAL PRIMARY KEY,
    streak_milestone INTEGER NOT NULL,  -- e.g., 3, 7, 14, 30 days
    item_id INTEGER REFERENCES item_types (item_id),
    quantity INTEGER DEFAULT 1,
    description TEXT
);
