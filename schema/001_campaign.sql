CREATE TABLE campaign (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    capture_date TIMESTAMP,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE campaign IS
'Logical acquisition campaign grouping BatteryView exports.';

COMMENT ON COLUMN campaign.capture_date IS
'Earliest export timestamp found among the files of the campaign.';