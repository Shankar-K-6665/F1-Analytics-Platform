-- =========================================================
-- FOREIGN KEY CONSTRAINTS
-- =========================================================

-- Race → Season
ALTER TABLE dim_race
ADD CONSTRAINT fk_race_season
FOREIGN KEY (season_year)
REFERENCES dim_season(season_year);


-- Race → Circuit
ALTER TABLE dim_race
ADD CONSTRAINT fk_race_circuit
FOREIGN KEY (circuit_id)
REFERENCES dim_circuit(circuit_id);


-- Race Result → Race
ALTER TABLE fact_race_result
ADD CONSTRAINT fk_result_race
FOREIGN KEY (race_id)
REFERENCES dim_race(race_id);


-- Race Result → Driver
ALTER TABLE fact_race_result
ADD CONSTRAINT fk_result_driver
FOREIGN KEY (driver_id)
REFERENCES dim_driver(driver_id);


-- Race Result → Constructor
ALTER TABLE fact_race_result
ADD CONSTRAINT fk_result_constructor
FOREIGN KEY (constructor_id)
REFERENCES dim_constructor(constructor_id);


-- Qualifying → Race
ALTER TABLE fact_qualifying
ADD CONSTRAINT fk_qualifying_race
FOREIGN KEY (race_id)
REFERENCES dim_race(race_id);


-- Qualifying → Driver
ALTER TABLE fact_qualifying
ADD CONSTRAINT fk_qualifying_driver
FOREIGN KEY (driver_id)
REFERENCES dim_driver(driver_id);


-- Qualifying → Constructor
ALTER TABLE fact_qualifying
ADD CONSTRAINT fk_qualifying_constructor
FOREIGN KEY (constructor_id)
REFERENCES dim_constructor(constructor_id);


-- Lap → Race
ALTER TABLE fact_lap
ADD CONSTRAINT fk_lap_race
FOREIGN KEY (race_id)
REFERENCES dim_race(race_id);


-- Lap → Driver
ALTER TABLE fact_lap
ADD CONSTRAINT fk_lap_driver
FOREIGN KEY (driver_id)
REFERENCES dim_driver(driver_id);


-- Pit Stop → Race
ALTER TABLE fact_pit_stop
ADD CONSTRAINT fk_pit_race
FOREIGN KEY (race_id)
REFERENCES dim_race(race_id);


-- Pit Stop → Driver
ALTER TABLE fact_pit_stop
ADD CONSTRAINT fk_pit_driver
FOREIGN KEY (driver_id)
REFERENCES dim_driver(driver_id);


-- Tyre → Race
ALTER TABLE fact_tyre
ADD CONSTRAINT fk_tyre_race
FOREIGN KEY (race_id)
REFERENCES dim_race(race_id);


-- Tyre → Driver
ALTER TABLE fact_tyre
ADD CONSTRAINT fk_tyre_driver
FOREIGN KEY (driver_id)
REFERENCES dim_driver(driver_id);


-- Weather → Race
ALTER TABLE fact_weather
ADD CONSTRAINT fk_weather_race
FOREIGN KEY (race_id)
REFERENCES dim_race(race_id);


-- Telemetry → Driver
ALTER TABLE fact_telemetry
ADD CONSTRAINT fk_telemetry_driver
FOREIGN KEY (driver_id)
REFERENCES dim_driver(driver_id);