-- =========================================================
-- F1 ANALYTICS PLATFORM
-- SQL VIEWS
-- =========================================================


-- =========================================================
-- DRIVER VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_driver_details AS
SELECT
    driver_id,
    driver_code,
    permanent_number,
    given_name,
    family_name,
    full_name,
    date_of_birth,
    nationality,
    driver_url
FROM dim_driver;


-- =========================================================
-- CONSTRUCTOR VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_constructor_details AS
SELECT
    constructor_id,
    constructor_name,
    nationality,
    constructor_url
FROM dim_constructor;


-- =========================================================
-- CIRCUIT VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_circuit_details AS
SELECT
    circuit_id,
    circuit_name,
    locality,
    country,
    latitude,
    longitude,
    circuit_url
FROM dim_circuit;


-- =========================================================
-- SEASON VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_season_details AS
SELECT
    season_year
FROM dim_season;


-- =========================================================
-- RACE VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_race_details AS
SELECT
    r.race_id,
    r.season_year,
    r.round_number,
    r.race_name,
    r.race_date,
    r.circuit_id,
    c.circuit_name,
    c.country,
    r.race_url
FROM dim_race r
LEFT JOIN dim_circuit c
    ON r.circuit_id = c.circuit_id;


-- =========================================================
-- DRIVER + CONSTRUCTOR VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_driver_constructor AS
SELECT
    d.driver_id,
    d.full_name,
    d.nationality AS driver_nationality,
    c.constructor_id,
    c.constructor_name,
    c.nationality AS constructor_nationality
FROM dim_driver d
CROSS JOIN dim_constructor c;


-- =========================================================
-- COMPLETE RACE RESULT VIEW
-- =========================================================

CREATE OR REPLACE VIEW vw_race_results AS
SELECT
    rr.result_id,

    r.race_id,
    r.season_year,
    r.round_number,
    r.race_name,
    r.race_date,

    d.driver_id,
    d.full_name AS driver_name,

    c.constructor_id,
    c.constructor_name,

    circuit.circuit_id,
    circuit.circuit_name,
    circuit.country,

    rr.grid_position,
    rr.finish_position,
    rr.position_text,
    rr.points,
    rr.laps_completed,
    rr.race_time,
    rr.status,

    rr.fastest_lap_number,
    rr.fastest_lap_time,
    rr.fastest_lap_speed

FROM fact_race_result rr

JOIN dim_race r
    ON rr.race_id = r.race_id

JOIN dim_driver d
    ON rr.driver_id = d.driver_id

JOIN dim_constructor c
    ON rr.constructor_id = c.constructor_id

LEFT JOIN dim_circuit circuit
    ON r.circuit_id = circuit.circuit_id;