CREATE INDEX idx_campaign_capture_date
    ON campaign(capture_date);

CREATE INDEX idx_export_timestamp
    ON campaign_export(export_timestamp);

CREATE INDEX idx_campaign_export_device
    ON campaign_export(device_id);

CREATE INDEX idx_device_snapshot_campaign_export
    ON device_snapshot(campaign_export_id);