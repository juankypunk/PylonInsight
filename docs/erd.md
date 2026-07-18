# Entity Relationship Diagram (ERD)

## Overview

This document describes the logical database model used by PylonInsight.

The goal of the data model is to separate:

* physical devices
* BatteryView acquisition campaigns
* exported data
* normalized records

The database stores a canonical representation of BatteryView exports rather than the original file structure.

---

# Entity Relationship Diagram

```text
                               +----------------------+
                               |      campaign        |
                               +----------------------+
                               | PK id               |
                               | name               |
                               | capture_date       |
                               | description        |
                               | created_at         |
                               +----------+---------+
                                          |
                                          | 1
                                          |
                                          | N
                               +----------v-----------+
                               |   campaign_device    |
                               +----------------------+
                               | PK id               |
                               | FK campaign_id      |
                               | FK device_id        |
                               | role               |
                               | device_address     |
                               | export_timestamp   |
                               | history_present    |
                               | events_present     |
                               | scanlog_present    |
                               | info_present       |
                               +----------+---------+
                                          |
                 +------------------------+-------------------------+
                 |                                                  |
                 | N                                                | 1
                 |                                                  |
      +----------v-----------+                           +----------v-----------+
      |       device         |                           |     environment      |
      +----------------------+                           +----------------------+
      | PK id               |                           | PK id               |
      | barcode UNIQUE      |                           | FK campaign_id      |
      | device_type         |                           | timestamp           |
      | manufacturer        |                           | ...                 |
      | specification       |                           +----------------------+
      | cell_count          |
      | notes               |
      +----------+----------+
                 |
                 | 1
                 |
                 | N
      +----------v-----------+
      |   device_snapshot    |
      +----------------------+
      | PK id               |
      | FK device_id        |
      | FK campaign_id      |
      | board_version       |
      | main_soft_version   |
      | soft_version        |
      | boot_version        |
      | comm_version        |
      | release_date        |
      +----------+----------+
                 |
      +----------+----------+-----------------------------+
      |                     |                             |
      |                     |                             |
+-----v----------+  +-------v---------+        +----------v---------+
| history_bms    |  | history_bmu     |        | history_xhb_bmu    |
+----------------+  +-----------------+        +--------------------+
| FK campaign... |  | FK campaign...  |        | FK campaign...     |
| timestamp      |  | timestamp       |        | timestamp          |
| ...            |  | ...             |        | ...                |
+----------------+  +-----------------+        +--------------------+

+----------------+  +-----------------+        +--------------------+
| event_bms      |  | event_bmu       |        | event_xhb_bmu      |
+----------------+  +-----------------+        +--------------------+
| FK campaign... |  | FK campaign...  |        | FK campaign...     |
| timestamp      |  | timestamp       |        | timestamp          |
| ...            |  | ...             |        | ...                |
+----------------+  +-----------------+        +--------------------+
```

---

# Entity Description

## campaign

Represents a logical acquisition campaign.

A campaign groups all BatteryView exports collected to characterize the complete battery system at a given point in time.

BatteryView has no native concept of a campaign; this abstraction is introduced by PylonInsight.

---

## campaign_device

Represents the participation of a physical device in a campaign.

It records:

* logical role (BMS, batt1, batt2, ...)
* communication address
* exported datasets
* export timestamp

This entity isolates campaign-specific information from the physical device identity.

---

## device

Represents a physical hardware device.

Devices are uniquely identified by their barcode (serial number).

A device exists independently of any campaign.

---

## device_snapshot

Represents the hardware and firmware configuration of a device during a specific campaign.

A snapshot preserves historical information even if firmware is updated later.

---

## history_*

Stores normalized historical measurements.

Different hardware generations use different schemas:

* history_bms
* history_bmu
* history_xhb_bmu

---

## event_*

Stores normalized event records.

Each hardware generation has its own schema.

---

## environment

Stores environmental or installation measurements associated with the campaign.

Typical information includes:

* inverter power
* operating mode
* external measurements
* user-provided environmental context

---

# Design Principles

The database follows these principles:

* Physical devices are independent from campaigns.
* Campaigns are logical groupings created by PylonInsight.
* BatteryView export peculiarities are handled during import.
* The database stores normalized data rather than raw CSV files.
* Different hardware generations use independent schemas whenever their data models differ.

---

# Future Extensions

Possible future entities include:

* import_session
* analysis_result
* finding
* user_annotation
* report

The current model has been designed so these entities can be added without modifying the existing relationships.
