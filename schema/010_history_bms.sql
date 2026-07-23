--
-- PylonInsight
-- history_bms
--
-- Historical measurements exported by BatteryView from the SC0500A BMS.
--

CREATE TABLE history_bms (

    id                  BIGSERIAL PRIMARY KEY,

    campaign_export_id  BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    record_timestamp    TIMESTAMP NOT NULL,

    stack_voltage_mv       INTEGER NOT NULL,
    stack_current_ma       INTEGER NOT NULL,

    temperature_c         INTEGER NOT NULL,

    battery_temp_low_c    INTEGER NOT NULL,
    battery_temp_high_c   INTEGER NOT NULL,

    battery_voltage_low_mv INTEGER NOT NULL,
    battery_voltage_high_mv INTEGER NOT NULL,

    unit_temp_low_c       INTEGER NOT NULL,
    unit_temp_high_c      INTEGER NOT NULL,

    unit_voltage_low_mv    INTEGER NOT NULL,
    unit_voltage_high_mv   INTEGER NOT NULL,

    base_state          TEXT NOT NULL,
    voltage_state       TEXT NOT NULL,
    current_state       TEXT NOT NULL,
    temperature_state   TEXT NOT NULL,

    state_of_charge     SMALLINT NOT NULL 
        CHECK (state_of_charge >= 0 AND state_of_charge <= 100),

    error_code          TEXT NOT NULL,

    events              TEXT NOT NULL,

    battery_events      TEXT,
    unit_events         TEXT,

    CONSTRAINT uq_history_bms
        UNIQUE (campaign_export_id, record_timestamp)

);

COMMENT ON TABLE history_bms IS
'Historical measurements exported by BatteryView from the SC0500A BMS.';

COMMENT ON COLUMN history_bms.campaign_export_id IS
'Reference to the BatteryView export that generated this record.';

COMMENT ON COLUMN history_bms.record_timestamp IS
'Timestamp reconstructed from the Date and Time columns exported by BatteryView.';

COMMENT ON COLUMN history_bms.stack_voltage_mv IS
'Total battery stack voltage (mV).';

COMMENT ON COLUMN history_bms.stack_current_ma IS
'Battery current (mA). Positive values indicate charging, negative values indicate discharging.';

COMMENT ON COLUMN history_bms.temperature_c IS
'Temperature value exported by BatteryView. Scaling currently under investigation.';

COMMENT ON COLUMN history_bms.battery_temp_low_c IS
'Battery low temperature related field.';

COMMENT ON COLUMN history_bms.battery_temp_high_c IS
'Battery high temperature related field.';

COMMENT ON COLUMN history_bms.battery_voltage_low_mv IS
'Battery low voltage related field. Exact meaning not yet confirmed.';

COMMENT ON COLUMN history_bms.battery_voltage_high_mv IS
'Battery high voltage related field. Exact meaning not yet confirmed.';

COMMENT ON COLUMN history_bms.unit_temp_low_c IS
'Unknown field exported by BatteryView.';

COMMENT ON COLUMN history_bms.unit_temp_high_c IS
'Unknown field exported by BatteryView.';

COMMENT ON COLUMN history_bms.unit_voltage_low_mv IS
'Module voltage related field. Exact meaning under investigation.';

COMMENT ON COLUMN history_bms.unit_voltage_high_mv   IS
'Module voltage related field. Exact meaning under investigation.';

COMMENT ON COLUMN history_bms.base_state IS
'Main operating state reported by the BMS.';

COMMENT ON COLUMN history_bms.voltage_state IS
'Voltage status reported by the BMS.';

COMMENT ON COLUMN history_bms.current_state IS
'Current status reported by the BMS.';

COMMENT ON COLUMN history_bms.temperature_state IS
'Temperature status reported by the BMS.';

COMMENT ON COLUMN history_bms.state_of_charge IS
'Battery State of Charge (SOC).';

COMMENT ON COLUMN history_bms.error_code IS
'BMS error code.';

COMMENT ON COLUMN history_bms.events IS
'System event flags exported by BatteryView.';

COMMENT ON COLUMN history_bms.battery_events IS
'Battery-specific event flags. Meaning currently unknown.';

COMMENT ON COLUMN history_bms.unit_events IS
'Unit-specific event flags. Meaning currently unknown.';

CREATE INDEX idx_history_bms_campaign_export
    ON history_bms(campaign_export_id);

CREATE INDEX idx_history_bms_timestamp
    ON history_bms(record_timestamp);

CREATE INDEX idx_history_bms_soc
    ON history_bms(state_of_charge);