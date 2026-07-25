# Import Process

## Overview

The PylonInsight importer is responsible for transforming a complete BatteryView acquisition campaign into a normalized PostgreSQL database.

The importer operates at **campaign level**, not at individual file level. A campaign represents a coherent set of BatteryView exports captured during the same acquisition session.

Each campaign may contain exports from one BMS and one or more battery modules (BMUs).

---

## Objectives

The importer must:

- Detect all exported devices.
- Register previously unknown devices.
- Preserve the original acquisition structure.
- Import historical measurements.
- Import event logs.
- Store device metadata.
- Be idempotent whenever possible.

---

## Expected campaign structure

A campaign directory contains one subdirectory per device.

Example:

```text
2026-07-08_SOC50/
│
├── BMS/
│   ├── history/
│   ├── events/
│   └── scanlog/
│
├── batt1/
│   ├── history/
│   ├── events/
│   └── scanlog/
│
├── batt2/
│   ├── history/
│   ├── events/
│   └── scanlog/
│
└── batt3/
    ├── history/
    ├── events/
    └── scanlog/
```

The importer shall not assume that every directory exists. BatteryView exports may contain only a subset of the available data.

---

## Import sequence

The recommended import order is:

1. Create the campaign.
2. Detect exported devices.
3. Register unknown devices.
4. Create campaign exports.
5. Extract and store device snapshots.
6. Import history datasets.
7. Import event datasets.
8. Import scanlog datasets (optional).

---

## Device discovery

Each device is uniquely identified by its barcode (serial number).

The importer shall:

- search the database for the barcode;
- create a new device if it does not exist;
- reuse the existing device otherwise.

This allows long-term tracking of the same physical battery across multiple campaigns.

---

## Campaign exports

Each exported device participating in a campaign creates one record in the `campaign_export` table.

The campaign role (BMS, batt1, batt2, batt3...) represents the physical position occupied during that campaign only.

The same physical module may occupy different positions in different campaigns.

---

## Device snapshot

BatteryView embeds device identification metadata in the header of several exported files (`history`, `history_detailed`, `event` and `event_detailed`).

The importer extracts this metadata and stores a normalized snapshot associated with the current campaign export.

This information includes firmware versions, hardware revision and device-specific attributes.

---

## History import

History files are imported into the corresponding normalized tables:

- history_bms
- history_bmu
- history_xhb_bmu

The timestamp is reconstructed from the Date and Time fields.

BatteryView omits the Date column from the CSV header. The importer shall compensate for this known export defect.

---

## Event import

Events are imported into the corresponding normalized tables:

- event_bms
- event_bmu
- event_xhb_bmu

Text files shall be decoded as UTF-16 Little Endian.

---

## Scanlog import

Scanlog import is optional.

If present, scanlog data shall be associated with the corresponding campaign export.

---

## Error handling

The importer should continue importing whenever possible.

Typical recoverable situations include:

- missing optional directories;
- missing scanlog exports;
- duplicated imports;
- empty event lists.

Corrupted or malformed files should generate warnings while preserving the remaining import process.

---

## Idempotency

Running the importer multiple times on the same campaign should not duplicate information.

The importer should detect previously imported entities whenever possible by using:

- device barcode;
- campaign identifier;
- unique timestamp constraints.

---

## Validation

The importer should perform basic consistency checks, including:

- duplicated timestamps;
- inconsistent device metadata;
- unexpected hardware type changes;
- malformed timestamps;
- invalid UTF-16 text files.

Warnings should be reported to the user but should not necessarily abort the import process.

---

## Future work

Future versions of the importer may include:

- automatic campaign discovery;
- incremental imports;
- checksum verification;
- import statistics;
- parallel processing;
- command line filtering by device or dataset.