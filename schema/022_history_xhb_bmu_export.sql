CREATE TABLE history_xhb_bmu_export (

    history_xhb_bmu_id BIGINT NOT NULL
        REFERENCES history_xhb_bmu(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    campaign_export_id BIGINT NOT NULL
        REFERENCES campaign_export(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    PRIMARY KEY (history_xhb_bmu_id, campaign_export_id)
);

CREATE INDEX idx_history_xhb_bmu_export_campaign_export
    ON history_xhb_bmu_export(campaign_export_id);