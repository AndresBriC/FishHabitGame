SELECT
    fish_id,
    name,
    rarity,
    catch_rate
FROM fish_list;

SELECT catch_rate FROM fish_list
WHERE name = 'Sea Bass';
