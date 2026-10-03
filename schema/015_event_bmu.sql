CREATE TABLE event_bmu (
    id                  BIGSERIAL PRIMARY KEY,
    campaign_export_id  BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    item                INTEGER NOT NULL,
    record_timestamp    TIMESTAMP NOT NULL,

    module_voltage_mv   INTEGER NOT NULL,
    module_temperature_c INTEGER NOT NULL,

    temperature_low_c   INTEGER NOT NULL,
    temperature_high_c  INTEGER NOT NULL,

    cell_voltage_low_mv  INTEGER NOT NULL,
    cell_voltage_high_mv INTEGER NOT NULL,

    voltage_state       TEXT NOT NULL,
    temperature_state   TEXT NOT NULL,

    events              TEXT NOT NULL,
    battery_events      TEXT,

    CONSTRAINT uq_event_bmu
        UNIQUE (campaign_export_id, item)
);

COMMENT ON TABLE event_bmu IS
'BMU event records exported by BatteryView.';

COMMENT ON COLUMN event_bmu.item IS
'Sequential record number assigned by BatteryView within the exported event file.';

COMMENT ON COLUMN event_bmu.record_timestamp IS
'Event timestamp reconstructed from the Date and Time fields of the BatteryView CSV.';

COMMENT ON COLUMN event_bmu.module_voltage_mv IS
'Module voltage in millivolts.';

COMMENT ON COLUMN event_bmu.module_temperature_c IS
'Module temperature in degrees Celsius.';

COMMENT ON COLUMN event_bmu.temperature_low_c IS
'Lowest module temperature reported by the BMU, in degrees Celsius.';

COMMENT ON COLUMN event_bmu.temperature_high_c IS
'Highest module temperature reported by the BMU, in degrees Celsius.';

COMMENT ON COLUMN event_bmu.cell_voltage_low_mv IS
'Lowest cell voltage reported by the BMU, in millivolts.';

COMMENT ON COLUMN event_bmu.cell_voltage_high_mv IS
'Highest cell voltage reported by the BMU, in millivolts.';

COMMENT ON COLUMN event_bmu.events IS
'BatteryView Events field. For the legacy BMU this field commonly contains the general status, such as Normal.';

COMMENT ON COLUMN event_bmu.battery_events IS
'BatteryView BatEvents field. This is the normalized event code for legacy BMU events.';

CREATE INDEX idx_event_bmu_timestamp
    ON event_bmu(record_timestamp);

CREATE INDEX idx_event_bmu_event_code
    ON event_bmu(battery_events);