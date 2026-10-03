CREATE TABLE event_bms (
    id                      BIGSERIAL PRIMARY KEY,
    campaign_export_id      BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    item                    INTEGER NOT NULL,
    record_timestamp        TIMESTAMP NOT NULL,

    stack_voltage_mv        INTEGER NOT NULL,
    stack_current_ma        INTEGER NOT NULL,
    temperature_c           INTEGER NOT NULL,

    battery_temp_low_c      INTEGER NOT NULL,
    battery_temp_high_c     INTEGER NOT NULL,

    battery_voltage_low_mv  INTEGER NOT NULL,
    battery_voltage_high_mv INTEGER NOT NULL,

    unit_temp_low_c         INTEGER NOT NULL,
    unit_temp_high_c        INTEGER NOT NULL,

    unit_voltage_low_mv     INTEGER NOT NULL,
    unit_voltage_high_mv    INTEGER NOT NULL,

    base_state              TEXT NOT NULL,
    voltage_state           TEXT NOT NULL,
    current_state           TEXT NOT NULL,
    temperature_state       TEXT NOT NULL,

    state_of_charge         SMALLINT NOT NULL
        CHECK (state_of_charge >= 0 AND state_of_charge <= 100),

    error_code              TEXT NOT NULL,

    events                  TEXT NOT NULL,
    battery_events          TEXT,
    unit_events             TEXT,

    CONSTRAINT uq_event_bms
        UNIQUE (campaign_export_id, item)
);

COMMENT ON TABLE event_bms IS
'BMS event records exported by BatteryView.';

COMMENT ON COLUMN event_bms.item IS
'Sequential record number assigned by BatteryView within the exported event file.';

COMMENT ON COLUMN event_bms.record_timestamp IS
'Event timestamp reconstructed from the Date and Time fields of the BatteryView CSV.';

COMMENT ON COLUMN event_bms.stack_voltage_mv IS
'Stack voltage in millivolts.';

COMMENT ON COLUMN event_bms.stack_current_ma IS
'Stack current in milliamperes.';

COMMENT ON COLUMN event_bms.temperature_c IS
'BMS temperature in degrees Celsius.';

COMMENT ON COLUMN event_bms.battery_temp_low_c IS
'Lowest battery temperature reported by the BMS, in degrees Celsius.';

COMMENT ON COLUMN event_bms.battery_temp_high_c IS
'Highest battery temperature reported by the BMS, in degrees Celsius.';

COMMENT ON COLUMN event_bms.battery_voltage_low_mv IS
'Lowest battery/module voltage reported by the BMS, in millivolts.';

COMMENT ON COLUMN event_bms.battery_voltage_high_mv IS
'Highest battery/module voltage reported by the BMS, in millivolts.';

COMMENT ON COLUMN event_bms.unit_temp_low_c IS
'Lowest unit temperature reported by the BMS, in degrees Celsius.';

COMMENT ON COLUMN event_bms.unit_temp_high_c IS
'Highest unit temperature reported by the BMS, in degrees Celsius.';

COMMENT ON COLUMN event_bms.unit_voltage_low_mv IS
'Lowest unit voltage reported by the BMS, in millivolts.';

COMMENT ON COLUMN event_bms.unit_voltage_high_mv IS
'Highest unit voltage reported by the BMS, in millivolts.';

COMMENT ON COLUMN event_bms.state_of_charge IS
'Battery state of charge as an integer percentage from 0 to 100.';

COMMENT ON COLUMN event_bms.error_code IS
'BatteryView BMS error code. The meaning of individual codes is documented separately.';

COMMENT ON COLUMN event_bms.events IS
'BatteryView Events field. This is the normalized event code for BMS events.';

COMMENT ON COLUMN event_bms.battery_events IS
'BatteryView BatEvents field.';

COMMENT ON COLUMN event_bms.unit_events IS
'BatteryView UnitEvents field.';


CREATE INDEX idx_event_bms_timestamp
    ON event_bms(record_timestamp);

CREATE INDEX idx_event_bms_event_code
    ON event_bms(events);

CREATE INDEX idx_event_bms_error_code
    ON event_bms(error_code);