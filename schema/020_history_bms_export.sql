CREATE TABLE history_bms_export (

    history_bms_id BIGINT NOT NULL
        REFERENCES history_bms(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    campaign_export_id BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    PRIMARY KEY (history_bms_id, campaign_export_id)
);

CREATE INDEX idx_history_bms_export_campaign_export
    ON history_bms_export(campaign_export_id);