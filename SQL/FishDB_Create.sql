CREATE DATABASE fish_game;

CREATE TABLE fish_list (
	fish_id serial PRIMARY key,
	name text UNIQUE not null,
	rarity text not null check (rarity in ('common', 'uncommon', 'rare', 'exotic')),
	catch_rate real not null check (catch_rate between 0 and 1)
);