-- =========================================================
-- F1 ANALYTICS PLATFORM
-- ANALYTICAL SQL QUERIES
-- =========================================================


-- =========================================================
-- 1. TOTAL NUMBER OF DRIVERS
-- =========================================================

SELECT
    COUNT(*) AS total_drivers
FROM dim_driver;


-- =========================================================
-- 2. TOTAL NUMBER OF CONSTRUCTORS
-- =========================================================

SELECT
    COUNT(*) AS total_constructors
FROM dim_constructor;


-- =========================================================
-- 3. TOTAL NUMBER OF CIRCUITS
-- =========================================================

SELECT
    COUNT(*) AS total_circuits
FROM dim_circuit;


-- =========================================================
-- 4. TOTAL NUMBER OF SEASONS
-- =========================================================

SELECT
    COUNT(*) AS total_seasons
FROM dim_season;


-- =========================================================
-- 5. DRIVERS BY NATIONALITY
-- =========================================================

SELECT
    nationality,
    COUNT(*) AS driver_count
FROM dim_driver
WHERE nationality IS NOT NULL
GROUP BY nationality
ORDER BY driver_count DESC;


-- =========================================================
-- 6. CONSTRUCTORS BY NATIONALITY
-- =========================================================

SELECT
    nationality,
    COUNT(*) AS constructor_count
FROM dim_constructor
WHERE nationality IS NOT NULL
GROUP BY nationality
ORDER BY constructor_count DESC;


-- =========================================================
-- 7. CIRCUITS BY COUNTRY
-- =========================================================

SELECT
    country,
    COUNT(*) AS circuit_count
FROM dim_circuit
WHERE country IS NOT NULL
GROUP BY country
ORDER BY circuit_count DESC;


-- =========================================================
-- 8. LIST ALL DRIVERS
-- =========================================================

SELECT
    driver_id,
    full_name,
    driver_code,
    nationality,
    date_of_birth
FROM dim_driver
ORDER BY full_name;


-- =========================================================
-- 9. LIST ALL CONSTRUCTORS
-- =========================================================

SELECT
    constructor_id,
    constructor_name,
    nationality
FROM dim_constructor
ORDER BY constructor_name;


-- =========================================================
-- 10. LIST ALL CIRCUITS
-- =========================================================

SELECT
    circuit_id,
    circuit_name,
    locality,
    country,
    latitude,
    longitude
FROM dim_circuit
ORDER BY circuit_name;


-- =========================================================
-- 11. OLDEST DRIVER
-- =========================================================

SELECT
    driver_id,
    full_name,
    date_of_birth,
    nationality
FROM dim_driver
WHERE date_of_birth IS NOT NULL
ORDER BY date_of_birth ASC
LIMIT 1;


-- =========================================================
-- 12. YOUNGEST DRIVER
-- =========================================================

SELECT
    driver_id,
    full_name,
    date_of_birth,
    nationality
FROM dim_driver
WHERE date_of_birth IS NOT NULL
ORDER BY date_of_birth DESC
LIMIT 1;


-- =========================================================
-- 13. DRIVERS BORN AFTER 1990
-- =========================================================

SELECT
    driver_id,
    full_name,
    date_of_birth,
    nationality
FROM dim_driver
WHERE date_of_birth >= '1990-01-01'
ORDER BY date_of_birth;


-- =========================================================
-- 14. DRIVERS BY NATIONALITY
-- WITH PERCENTAGE
-- =========================================================

SELECT
    nationality,
    COUNT(*) AS driver_count,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM dim_driver
WHERE nationality IS NOT NULL
GROUP BY nationality
ORDER BY driver_count DESC;


-- =========================================================
-- 15. CIRCUITS WITH COORDINATES
-- =========================================================

SELECT
    circuit_name,
    locality,
    country,
    latitude,
    longitude
FROM dim_circuit
WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
ORDER BY country, circuit_name;


-- =========================================================
-- 16. RACES BY SEASON
-- =========================================================

SELECT
    season_year,
    COUNT(*) AS race_count
FROM dim_race
GROUP BY season_year
ORDER BY season_year;


-- =========================================================
-- 17. RACES BY COUNTRY
-- =========================================================

SELECT
    c.country,
    COUNT(*) AS race_count
FROM dim_race r
JOIN dim_circuit c
    ON r.circuit_id = c.circuit_id
GROUP BY c.country
ORDER BY race_count DESC;


-- =========================================================
-- 18. TOTAL RACE RESULTS
-- =========================================================

SELECT
    COUNT(*) AS total_race_results
FROM fact_race_result;


-- =========================================================
-- 19. DRIVER TOTAL POINTS
-- =========================================================

SELECT
    d.driver_id,
    d.full_name,
    SUM(rr.points) AS total_points
FROM fact_race_result rr
JOIN dim_driver d
    ON rr.driver_id = d.driver_id
GROUP BY
    d.driver_id,
    d.full_name
ORDER BY total_points DESC;


-- =========================================================
-- 20. DRIVER WINS
-- =========================================================

SELECT
    d.driver_id,
    d.full_name,
    COUNT(*) AS race_wins
FROM fact_race_result rr
JOIN dim_driver d
    ON rr.driver_id = d.driver_id
WHERE rr.finish_position = 1
GROUP BY
    d.driver_id,
    d.full_name
ORDER BY race_wins DESC;


-- =========================================================
-- 21. DRIVER PODIUMS
-- =========================================================

SELECT
    d.driver_id,
    d.full_name,
    COUNT(*) AS podiums
FROM fact_race_result rr
JOIN dim_driver d
    ON rr.driver_id = d.driver_id
WHERE rr.finish_position BETWEEN 1 AND 3
GROUP BY
    d.driver_id,
    d.full_name
ORDER BY podiums DESC;


-- =========================================================
-- 22. CONSTRUCTOR TOTAL POINTS
-- =========================================================

SELECT
    c.constructor_id,
    c.constructor_name,
    SUM(rr.points) AS total_points
FROM fact_race_result rr
JOIN dim_constructor c
    ON rr.constructor_id = c.constructor_id
GROUP BY
    c.constructor_id,
    c.constructor_name
ORDER BY total_points DESC;


-- =========================================================
-- 23. CONSTRUCTOR WINS
-- =========================================================

SELECT
    c.constructor_id,
    c.constructor_name,
    COUNT(*) AS race_wins
FROM fact_race_result rr
JOIN dim_constructor c
    ON rr.constructor_id = c.constructor_id
WHERE rr.finish_position = 1
GROUP BY
    c.constructor_id,
    c.constructor_name
ORDER BY race_wins DESC;


-- =========================================================
-- 24. DRIVER PERFORMANCE BY SEASON
-- =========================================================

SELECT
    r.season_year,
    d.full_name,
    SUM(rr.points) AS season_points,
    COUNT(*) FILTER (
        WHERE rr.finish_position = 1
    ) AS wins,

    COUNT(*) FILTER (
        WHERE rr.finish_position BETWEEN 1 AND 3
    ) AS podiums

FROM fact_race_result rr

JOIN dim_race r
    ON rr.race_id = r.race_id

JOIN dim_driver d
    ON rr.driver_id = d.driver_id

GROUP BY
    r.season_year,
    d.full_name

ORDER BY
    r.season_year,
    season_points DESC;


-- =========================================================
-- 25. DNFs BY DRIVER
-- =========================================================

SELECT
    d.driver_id,
    d.full_name,
    COUNT(*) AS dnfs
FROM fact_race_result rr
JOIN dim_driver d
    ON rr.driver_id = d.driver_id
WHERE rr.status NOT IN (
    'Finished',
    '+1 Lap',
    '+2 Laps',
    '+3 Laps'
)
GROUP BY
    d.driver_id,
    d.full_name
ORDER BY dnfs DESC;