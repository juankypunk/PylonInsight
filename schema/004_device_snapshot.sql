CREATE TABLE device_snapshot (

    id                      BIGSERIAL PRIMARY KEY,

    campaign_export_id       BIGINT NOT NULL
                                REFERENCES campaign_export(id) ON UPDATE CASCADE ON DELETE CASCADE,

    board_version           VARCHAR(50),

    hardware_version        VARCHAR(30),

    main_soft_version       VARCHAR(30),

    soft_version            VARCHAR(30),

    sub_soft_version        VARCHAR(30),

    boot_version            VARCHAR(30),

    comm_version            VARCHAR(30),

    release_date            DATE,

    module_afetype          VARCHAR(30),

    module_celltype         VARCHAR(30),

    fan_exist               BOOLEAN,

    xhb_v3_board            BOOLEAN
);