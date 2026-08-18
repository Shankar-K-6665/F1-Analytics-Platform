-- =========================================================
-- INDEXES FOR PERFORMANCE
-- =========================================================

CREATE INDEX idx_driver_nationality
ON dim_driver(nationality);


CREATE INDEX idx_constructor_nationality
ON dim_constructor(nationality);


CREATE INDEX idx_circuit_country
ON dim_circuit(country);


CREATE INDEX idx_race_season
ON dim_race(season_year);


CREATE INDEX idx_race_circuit
ON dim_race(circuit_id);


CREATE INDEX idx_result_driver
ON fact_race_result(driver_id);


CREATE INDEX idx_result_constructor
ON fact_race_result(constructor_id);


CREATE INDEX idx_result_race
ON fact_race_result(race_id);


CREATE INDEX idx_qualifying_driver
ON fact_qualifying(driver_id);


CREATE INDEX idx_lap_driver
ON fact_lap(driver_id);


CREATE INDEX idx_pit_driver
ON fact_pit_stop(driver_id);


CREATE INDEX idx_tyre_driver
ON fact_tyre(driver_id);


CREATE INDEX idx_telemetry_driver
ON fact_telemetry(driver_id);