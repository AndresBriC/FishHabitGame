CREATE DATABASE fish_game;

CREATE TABLE fish_list (
    fish_id serial PRIMARY KEY,
    name text UNIQUE NOT NULL,
    rarity text NOT NULL CHECK (
        rarity IN ('common', 'uncommon', 'rare', 'exotic')
    ),
    catch_rate real NOT NULL CHECK (catch_rate BETWEEN 0 AND 1)
);
