-- =========================================================
-- FORMULA 1 ANALYTICS PLATFORM
-- DATABASE SCHEMA
-- =========================================================

-- =========================================================
-- DIMENSION: DRIVER
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_driver (
    driver_id VARCHAR(50) PRIMARY KEY,
    driver_code VARCHAR(10),
    permanent_number VARCHAR(10),
    given_name VARCHAR(100) NOT NULL,
    family_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    date_of_birth DATE,
    nationality VARCHAR(100),
    driver_url TEXT
);


-- =========================================================
-- DIMENSION: CONSTRUCTOR
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_constructor (
    constructor_id VARCHAR(50) PRIMARY KEY,
    constructor_name VARCHAR(150) NOT NULL,
    nationality VARCHAR(100),
    constructor_url TEXT
);


-- =========================================================
-- DIMENSION: CIRCUIT
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_circuit (
    circuit_id VARCHAR(50) PRIMARY KEY,
    circuit_name VARCHAR(200) NOT NULL,
    locality VARCHAR(150),
    country VARCHAR(100),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    circuit_url TEXT
);


-- =========================================================
-- DIMENSION: SEASON
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_season (
    season_year INTEGER PRIMARY KEY
);


-- =========================================================
-- DIMENSION: RACE
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_race (
    race_id INTEGER PRIMARY KEY,
    season_year INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    race_name VARCHAR(200) NOT NULL,
    race_date DATE,
    circuit_id VARCHAR(50),
    race_url TEXT,

    CONSTRAINT uq_race_season_round
        UNIQUE (season_year, round_number)
);

-- =========================================================
-- FACT: RACE RESULT
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_race_result (
    result_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER NOT NULL,
    driver_id VARCHAR(50) NOT NULL,
    constructor_id VARCHAR(50) NOT NULL,

    grid_position INTEGER,
    finish_position INTEGER,
    position_text VARCHAR(20),

    points DECIMAL(8,2),
    laps_completed INTEGER,

    race_time VARCHAR(50),
    status VARCHAR(100),

    fastest_lap_number INTEGER,
    fastest_lap_time VARCHAR(30),
    fastest_lap_speed DECIMAL(8,3),

    UNIQUE (race_id, driver_id)
);


-- =========================================================
-- FACT: QUALIFYING
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_qualifying (
    qualifying_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER NOT NULL,
    driver_id VARCHAR(50) NOT NULL,
    constructor_id VARCHAR(50) NOT NULL,

    qualifying_position INTEGER,

    q1_time VARCHAR(30),
    q2_time VARCHAR(30),
    q3_time VARCHAR(30),

    UNIQUE (race_id, driver_id)
);


-- =========================================================
-- FACT: LAP
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_lap (
    lap_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER NOT NULL,
    driver_id VARCHAR(50) NOT NULL,

    lap_number INTEGER NOT NULL,

    lap_time VARCHAR(30),
    sector_1_time VARCHAR(30),
    sector_2_time VARCHAR(30),
    sector_3_time VARCHAR(30),

    average_speed DECIMAL(8,3),

    UNIQUE (race_id, driver_id, lap_number)
);


-- =========================================================
-- FACT: PIT STOP
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_pit_stop (
    pit_stop_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER NOT NULL,
    driver_id VARCHAR(50) NOT NULL,

    stop_number INTEGER,
    lap_number INTEGER,

    pit_time VARCHAR(30),
    pit_duration DECIMAL(8,3),

    UNIQUE (race_id, driver_id, stop_number)
);


-- =========================================================
-- FACT: TYRE
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_tyre (
    tyre_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER NOT NULL,
    driver_id VARCHAR(50) NOT NULL,

    lap_start INTEGER,
    lap_end INTEGER,

    compound VARCHAR(30),
    tyre_stint INTEGER,

    UNIQUE (
        race_id,
        driver_id,
        tyre_stint
    )
);


-- =========================================================
-- FACT: WEATHER
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_weather (
    weather_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER NOT NULL,

    timestamp TIMESTAMP,

    air_temperature DECIMAL(6,2),
    track_temperature DECIMAL(6,2),

    humidity DECIMAL(6,2),
    pressure DECIMAL(8,2),

    rainfall DECIMAL(8,3),
    wind_speed DECIMAL(8,3),
    wind_direction DECIMAL(8,3)
);


-- =========================================================
-- FACT: TELEMETRY
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_telemetry (
    telemetry_id BIGSERIAL PRIMARY KEY,

    race_id INTEGER,
    driver_id VARCHAR(50) NOT NULL,

    session_type VARCHAR(20),

    timestamp TIMESTAMP,

    distance DECIMAL(10,3),

    speed DECIMAL(8,3),
    rpm INTEGER,
    gear INTEGER,

    throttle DECIMAL(6,2),
    brake DECIMAL(6,2),

    drs INTEGER,

    x_position DECIMAL(12,6),
    y_position DECIMAL(12,6),
    z_position DECIMAL(12,6)
);