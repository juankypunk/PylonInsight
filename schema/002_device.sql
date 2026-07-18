CREATE TYPE device_type AS ENUM (
    'BMS',
    'BMU',
    'XHB_BMU'
);


CREATE TABLE device (
    id                  BIGSERIAL PRIMARY KEY,
    barcode             VARCHAR(64) NOT NULL UNIQUE,
    device_type         device_type NOT NULL,
    manufacturer        VARCHAR(50),
    specification       VARCHAR(50), 
    cell_count          SMALLINT,
    notes               TEXT
);

