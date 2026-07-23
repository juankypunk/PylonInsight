--
-- PylonInsight
-- history_bmu
--
-- Historical measurements exported by BatteryView from first-generation BMU
-- (Device name: bmu, Board version: HP0115SV10R01).
--

CREATE TABLE history_bmu (

    id                  BIGSERIAL PRIMARY KEY,

    campaign_export_id  BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    record_timestamp    TIMESTAMP NOT NULL,

    module_voltage_mv      INTEGER NOT NULL,

    module_temperature_c  INTEGER NOT NULL,

    temperature_low_c     INTEGER NOT NULL,

    temperature_high_c     INTEGER NOT NULL,

    cell_voltage_low_mv    INTEGER NOT NULL,

    cell_voltage_high_mv   INTEGER NOT NULL,

    voltage_state       TEXT NOT NULL,

    temperature_state   TEXT NOT NULL,

    events              TEXT,

    battery_events      TEXT,

    CONSTRAINT uq_history_bmu
        UNIQUE (campaign_export_id, record_timestamp)

);

COMMENT ON TABLE history_bmu IS
'Historical measurements exported by BatteryView from first-generation BMU devices.';

COMMENT ON COLUMN history_bmu.campaign_export_id IS
'Reference to the BatteryView export that generated this record.';

COMMENT ON COLUMN history_bmu.record_timestamp IS
'Timestamp reconstructed from the Date and Time columns exported by BatteryView.';

COMMENT ON COLUMN history_bmu.module_voltage_mv IS
'Module voltage (mV).';

COMMENT ON COLUMN history_bmu.module_temperature_c IS
'Temperature-related value exported by BatteryView. Exact scaling under investigation.';

COMMENT ON COLUMN history_bmu.temperature_low_c IS
'Lower temperature value or threshold.';

COMMENT ON COLUMN history_bmu.temperature_high_c IS
'Upper temperature value or threshold.';

COMMENT ON COLUMN history_bmu.cell_voltage_low_mv IS
'Lowest cell voltage recorded within the module (mV).';

COMMENT ON COLUMN history_bmu.cell_voltage_high_mv IS
'Highest cell voltage recorded within the module (mV).';

COMMENT ON COLUMN history_bmu.voltage_state IS
'Voltage status reported by the BMU.';

COMMENT ON COLUMN history_bmu.temperature_state IS
'Temperature status reported by the BMU.';

COMMENT ON COLUMN history_bmu.events IS
'General BMU event flags. No values observed in analysed datasets.';

COMMENT ON COLUMN history_bmu.battery_events IS
'Battery-specific event flags. Meaning currently under investigation.';

CREATE INDEX idx_history_bmu_campaign_export
    ON history_bmu(campaign_export_id);

CREATE INDEX idx_history_bmu_timestamp
    ON history_bmu(record_timestamp);