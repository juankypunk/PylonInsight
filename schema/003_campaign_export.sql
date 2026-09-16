CREATE TYPE campaign_role AS ENUM (
    'BMS',
    'BMU1',
    'BMU2',
    'BMU3',
    'BMU4',
    'BMU5',
    'BMU6',
    'BMU7',
    'BMU8',
    'BMU9',
    'BMU10'
);


CREATE TABLE campaign_export (

    id                  BIGSERIAL PRIMARY KEY,

    campaign_id         BIGINT NOT NULL
                            REFERENCES campaign(id) ON UPDATE CASCADE ON DELETE RESTRICT,

    device_id           BIGINT NOT NULL
                            REFERENCES device(id) ON UPDATE CASCADE ON DELETE RESTRICT,

    role                campaign_role NOT NULL,

    export_timestamp    TIMESTAMP,

    history_present     BOOLEAN NOT NULL DEFAULT FALSE,

    events_present      BOOLEAN NOT NULL DEFAULT FALSE,

    info_present        BOOLEAN NOT NULL DEFAULT FALSE,

    scanlog_present     BOOLEAN NOT NULL DEFAULT FALSE,

    UNIQUE(campaign_id, role)
);


