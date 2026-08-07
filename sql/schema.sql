-- PostgreSQL / PostGIS DDL Schema for India EV Charging Platform

CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. EV Charging Stations Table
CREATE TABLE IF NOT EXISTS ev_charging_stations (
    station_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    operator VARCHAR(100),
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    connectors INT,
    kw_power DOUBLE PRECISION,
    charger_type VARCHAR(100),
    status VARCHAR(50),
    cost_per_kwh_inr DOUBLE PRECISION,
    is_24x7 BOOLEAN,
    geom GEOMETRY(Point, 4326)
);

-- 2. Vahan EV Registration Metrics Table
CREATE TABLE IF NOT EXISTS vahan_ev_registrations (
    record_id VARCHAR(50) PRIMARY KEY,
    state VARCHAR(100),
    district VARCHAR(100),
    rto_code VARCHAR(20),
    vehicle_category VARCHAR(100),
    year INT,
    month VARCHAR(20),
    ev_registrations INT,
    total_registrations INT,
    ev_penetration_pct DOUBLE PRECISION,
    yoy_growth_pct DOUBLE PRECISION
);

-- 3. Points of Interest (Commercial & Transit Hubs) Table
CREATE TABLE IF NOT EXISTS points_of_interest (
    poi_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    footfall_index INT,
    parking_capacity INT,
    has_high_voltage_power BOOLEAN,
    geom GEOMETRY(Point, 4326)
);

-- 4. Power Substations Table
CREATE TABLE IF NOT EXISTS power_substations (
    substation_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    voltage_kv INT,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    spare_capacity_mw DOUBLE PRECISION,
    grid_reliability_pct DOUBLE PRECISION,
    geom GEOMETRY(Point, 4326)
);

-- 5. Highway Corridors Table
CREATE TABLE IF NOT EXISTS highway_corridors (
    highway_id VARCHAR(50) PRIMARY KEY,
    highway_name VARCHAR(50),
    segment_id INT,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    daily_traffic_volume INT,
    freight_percentage DOUBLE PRECISION,
    nearest_charger_dist_km DOUBLE PRECISION,
    charging_desert_flag BOOLEAN,
    geom GEOMETRY(Point, 4326)
);

-- Spatial Views
CREATE OR REPLACE VIEW view_charging_deserts AS
SELECT 
    h.highway_id,
    h.highway_name,
    h.daily_traffic_volume,
    h.nearest_charger_dist_km,
    h.lat,
    h.lon
FROM highway_corridors h
WHERE h.nearest_charger_dist_km > 15.0 AND h.daily_traffic_volume > 20000;
