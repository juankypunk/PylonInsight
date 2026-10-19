CREATE TABLE history_bmu_export (

    history_bmu_id BIGINT NOT NULL
        REFERENCES history_bmu(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    campaign_export_id BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    PRIMARY KEY (history_bmu_id, campaign_export_id)
);

CREATE INDEX idx_history_bmu_export_campaign_export
    ON history_bmu_export(campaign_export_id);