INSERT INTO daily_pond (user_id, fish_id)
VALUES (
    'user_id',
    1
);


ALTER TABLE users
ADD COLUMN pond_size INTEGER DEFAULT 3;

ALTER TABLE daily_pond
ALTER COLUMN expires_at SET DEFAULT (CURRENT_DATE + INTERVAL '1 day');

UPDATE users
SET pond_size = 3
WHERE pond_size IS NULL;

--SELECT * FROM users;

--SELECT * FROM daily_pond;
DELETE FROM daily_pond;

SELECT
    user_id,
    username,
    fishing_attempts_left,
    fishing_attempts_reset_at,
    pond_size,
    current_rod_id
FROM users
WHERE user_id = 'user_id';

SELECT fish_id FROM daily_pond
WHERE user_id = 'user_id' AND expires_at > CURRENT_DATE;

SELECT ft.name
FROM daily_pond AS dp
INNER JOIN fish_types AS ft ON dp.fish_id = ft.fish_id
WHERE
    dp.user_id = 'user_id'
    AND dp.expires_at > CURRENT_DATE;


SELECT
    dp.fish_id,
    ft.name
FROM daily_pond AS dp
INNER JOIN fish_types AS ft ON dp.fish_id = ft.fish_id
WHERE
    dp.user_id = 'user_id'
    AND dp.expires_at > CURRENT_DATE;
