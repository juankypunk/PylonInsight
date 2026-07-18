CREATE INDEX idx_campaign_capture_date
ON campaign(capture_date);

CREATE INDEX idx_device_barcode
ON device(barcode);

CREATE INDEX idx_export_timestamp
ON campaign_export(export_timestamp);
