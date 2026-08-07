-- Spatial GiST and Attribute Indexes for High Performance Geospatial Queries

CREATE INDEX IF NOT EXISTS idx_ev_chargers_geom ON ev_charging_stations USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_ev_chargers_state_district ON ev_charging_stations (state, district);

CREATE INDEX IF NOT EXISTS idx_vahan_state_district ON vahan_ev_registrations (state, district, year);

CREATE INDEX IF NOT EXISTS idx_pois_geom ON points_of_interest USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_pois_category ON points_of_interest (category);

CREATE INDEX IF NOT EXISTS idx_substations_geom ON power_substations USING GIST (geom);

CREATE INDEX IF NOT EXISTS idx_highways_geom ON highway_corridors USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_highways_name ON highway_corridors (highway_name);
