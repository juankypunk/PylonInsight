--
-- PylonInsight
-- history_xhb_bmu
--
-- Historical measurements exported by BatteryView from XHB_BMU_NT modules.
--

CREATE TABLE history_xhb_bmu (

    id                          BIGSERIAL PRIMARY KEY,

    campaign_export_id          BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    record_timestamp            TIMESTAMP NOT NULL,

    module_voltage_mv           INTEGER NOT NULL,

    module_temperature_c        INTEGER NOT NULL,

    battery_temperature_low_c   INTEGER NOT NULL,

    battery_temperature_high_c  INTEGER NOT NULL,

    cell_voltage_low_mv         INTEGER NOT NULL,

    cell_voltage_high_mv        INTEGER NOT NULL,

    positive_terminal_temperature_c INTEGER NOT NULL,

    negative_terminal_temperature_c INTEGER NOT NULL,

    reference_voltage_mv        INTEGER NOT NULL,

    fan_pwm                     INTEGER NOT NULL,

    fan1_rpm                    INTEGER NOT NULL,

    fan2_rpm                    INTEGER NOT NULL,

    base_state                  TEXT NOT NULL,

    voltage_state               TEXT NOT NULL,

    temperature_state           TEXT NOT NULL,

    positive_terminal_temperature_state TEXT NOT NULL,

    negative_terminal_temperature_state TEXT NOT NULL,

    error_code                  TEXT NOT NULL,

    events                      TEXT,

    CONSTRAINT uq_history_xhb_bmu
        UNIQUE (campaign_export_id, record_timestamp)

);

COMMENT ON TABLE history_xhb_bmu IS
'Historical measurements exported by BatteryView from XHB_BMU_NT battery modules.';

COMMENT ON COLUMN history_xhb_bmu.campaign_export_id IS
'Reference to the BatteryView export that generated this record.';

COMMENT ON COLUMN history_xhb_bmu.record_timestamp IS
'Timestamp reconstructed from the Date and Time columns exported by BatteryView. The Date column is missing from the CSV header due to a BatteryView export bug but is present in every record.';

COMMENT ON COLUMN history_xhb_bmu.module_voltage_mv IS
'Module voltage (mV).';

COMMENT ON COLUMN history_xhb_bmu.module_temperature_c IS
'Temperature-related value exported by BatteryView. Exact scaling under investigation.';

COMMENT ON COLUMN history_xhb_bmu.battery_temperature_low_c IS
'Lower battery temperature value or threshold.';

COMMENT ON COLUMN history_xhb_bmu.battery_temperature_high_c IS
'Upper battery temperature value or threshold.';

COMMENT ON COLUMN history_xhb_bmu.cell_voltage_low_mv IS
'Lowest cell voltage recorded within the module (mV).';

COMMENT ON COLUMN history_xhb_bmu.cell_voltage_high_mv IS
'Highest cell voltage recorded within the module (mV).';

COMMENT ON COLUMN history_xhb_bmu.positive_terminal_temperature_c IS
'Temperature measured near the positive power terminal.';

COMMENT ON COLUMN history_xhb_bmu.negative_terminal_temperature_c IS
'Temperature measured near the negative power terminal.';

COMMENT ON COLUMN history_xhb_bmu.reference_voltage_mv IS
'Internal reference voltage reported by the BMU. Exact meaning under investigation.';

COMMENT ON COLUMN history_xhb_bmu.fan_pwm IS
'PWM duty cycle applied to the cooling fan.';

COMMENT ON COLUMN history_xhb_bmu.fan1_rpm IS
'Fan 1 rotational speed (rpm).';

COMMENT ON COLUMN history_xhb_bmu.fan2_rpm IS
'Fan 2 rotational speed (rpm).';

COMMENT ON COLUMN history_xhb_bmu.base_state IS
'Main operating state reported by the BMU.';

COMMENT ON COLUMN history_xhb_bmu.voltage_state IS
'Voltage status reported by the BMU.';

COMMENT ON COLUMN history_xhb_bmu.temperature_state IS
'Internal temperature status reported by the BMU.';

COMMENT ON COLUMN history_xhb_bmu.positive_terminal_temperature_state IS
'Status of the positive terminal temperature measurement.';

COMMENT ON COLUMN history_xhb_bmu.negative_terminal_temperature_state IS
'Status of the negative terminal temperature measurement.';

COMMENT ON COLUMN history_xhb_bmu.error_code IS
'BMU error code.';

COMMENT ON COLUMN history_xhb_bmu.events IS
'General event flags exported by BatteryView.';

CREATE INDEX idx_history_xhb_bmu_campaign_export
    ON history_xhb_bmu(campaign_export_id);

CREATE INDEX idx_history_xhb_bmu_timestamp
    ON history_xhb_bmu(record_timestamp);