CREATE TABLE event_xhb_bmu (
    id                                  BIGSERIAL PRIMARY KEY,
    campaign_export_id                  BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    item                                INTEGER NOT NULL,
    record_timestamp                    TIMESTAMP NOT NULL,

    module_voltage_mv                   INTEGER NOT NULL,
    module_temperature_c                INTEGER NOT NULL,

    battery_temperature_low_c           INTEGER NOT NULL,
    battery_temperature_high_c          INTEGER NOT NULL,

    cell_voltage_low_mv                 INTEGER NOT NULL,
    cell_voltage_high_mv                INTEGER NOT NULL,

    positive_terminal_temperature_c     INTEGER NOT NULL,
    negative_terminal_temperature_c     INTEGER NOT NULL,

    reference_voltage_mv                INTEGER NOT NULL,

    fan_pwm                             INTEGER NOT NULL,
    fan1_rpm                            INTEGER NOT NULL,
    fan2_rpm                            INTEGER NOT NULL,

    base_state                          TEXT NOT NULL,
    voltage_state                       TEXT NOT NULL,
    temperature_state                   TEXT NOT NULL,
    positive_terminal_temperature_state TEXT NOT NULL,
    negative_terminal_temperature_state TEXT NOT NULL,

    error_code                          TEXT NOT NULL,

    events                              TEXT NOT NULL,

    CONSTRAINT uq_event_xhb_bmu
        UNIQUE (campaign_export_id, item)
);

COMMENT ON TABLE event_xhb_bmu IS
'XHB BMU event records exported by BatteryView.';

COMMENT ON COLUMN event_xhb_bmu.item IS
'Sequential record number assigned by BatteryView within the exported event file.';

COMMENT ON COLUMN event_xhb_bmu.record_timestamp IS
'Event timestamp reconstructed from the Date and Time fields of the BatteryView CSV.';

COMMENT ON COLUMN event_xhb_bmu.module_voltage_mv IS
'Module voltage in millivolts.';

COMMENT ON COLUMN event_xhb_bmu.module_temperature_c IS
'Module temperature in degrees Celsius.';

COMMENT ON COLUMN event_xhb_bmu.battery_temperature_low_c IS
'Lowest battery temperature reported by the XHB BMU, in degrees Celsius.';

COMMENT ON COLUMN event_xhb_bmu.battery_temperature_high_c IS
'Highest battery temperature reported by the XHB BMU, in degrees Celsius.';

COMMENT ON COLUMN event_xhb_bmu.cell_voltage_low_mv IS
'Lowest cell voltage reported by the XHB BMU, in millivolts.';

COMMENT ON COLUMN event_xhb_bmu.cell_voltage_high_mv IS
'Highest cell voltage reported by the XHB BMU, in millivolts.';

COMMENT ON COLUMN event_xhb_bmu.positive_terminal_temperature_c IS
'Positive terminal temperature in degrees Celsius.';

COMMENT ON COLUMN event_xhb_bmu.negative_terminal_temperature_c IS
'Negative terminal temperature in degrees Celsius.';

COMMENT ON COLUMN event_xhb_bmu.reference_voltage_mv IS
'Reference voltage reported by the XHB BMU, in millivolts.';

COMMENT ON COLUMN event_xhb_bmu.fan_pwm IS
'Fan PWM value reported by the XHB BMU.';

COMMENT ON COLUMN event_xhb_bmu.fan1_rpm IS
'Fan 1 rotational speed in revolutions per minute.';

COMMENT ON COLUMN event_xhb_bmu.fan2_rpm IS
'Fan 2 rotational speed in revolutions per minute.';

COMMENT ON COLUMN event_xhb_bmu.events IS
'BatteryView Events field. This is the normalized event code for XHB BMU events.';

COMMENT ON COLUMN event_xhb_bmu.error_code IS
'BatteryView XHB BMU error code. The meaning of individual codes is documented separately.';

CREATE INDEX idx_event_xhb_bmu_timestamp
    ON event_xhb_bmu(record_timestamp);

CREATE INDEX idx_event_xhb_bmu_event_code
    ON event_xhb_bmu(events);

CREATE INDEX idx_event_xhb_bmu_error_code
    ON event_xhb_bmu(error_code);