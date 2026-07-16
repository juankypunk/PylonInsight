# PylonInsight Architecture

## Overview

PylonInsight is designed as a modular data analysis platform for Pylontech battery systems.

Its primary objective is to transform BatteryView exports into a normalized database that enables long-term analysis, reverse engineering and fault diagnosis.

The architecture intentionally separates four independent layers:

* Data acquisition
* Data normalization
* Persistent storage
* Analysis

This separation allows new BatteryView versions, firmware revisions or hardware generations to be supported without affecting the analysis layer.

---

# Architecture

```text
                BatteryView exports
                       │
        ┌──────────────┴──────────────┐
        │                             │
     history.*                    events.*
     info.*                       environment.*
        │
        ▼
+---------------------------+
| Import / Parsing Engine   |
+---------------------------+
        │
        │ UTF-16 decoding
        │ CSV parsing
        │ Header correction
        │ Timestamp reconstruction
        │ Device detection
        │ Validation
        │
        ▼
+---------------------------+
| Normalized Data Model     |
+---------------------------+
        │
        ▼
+---------------------------+
| PostgreSQL Database       |
+---------------------------+
        │
        ├── Campaigns
        ├── Devices
        ├── History
        ├── Events
        ├── Environment
        └── Metadata
        │
        ▼
+---------------------------+
| Analysis Engine           |
+---------------------------+
        │
        ├── Cell imbalance
        ├── Capacity estimation
        ├── Internal resistance
        ├── Event correlation
        ├── Fault detection
        ├── Trend analysis
        └── Reporting
```

---

# Main Components

## Import Engine

Responsible for reading BatteryView exports.

Responsibilities:

* UTF-16 decoding
* CSV parsing
* automatic device identification
* validation
* timestamp reconstruction
* correction of known BatteryView export inconsistencies
* incremental import

---

## Normalization Layer

Converts BatteryView exports into a consistent internal representation.

Examples:

* reconstruct missing `Date` header in `event.csv`
* normalize timestamps
* map hardware-specific field names
* validate record integrity

This layer isolates the rest of the project from BatteryView-specific quirks.

---

## Database

PostgreSQL is used as the canonical data repository.

The database stores normalized information rather than raw BatteryView files.

The original exports remain available for auditing purposes.

---

## Analysis Engine

This component derives information from historical data.

Planned analyses include:

* voltage imbalance
* temperature distribution
* module comparison
* battery ageing
* event correlation
* anomaly detection
* firmware comparison
* hardware comparison

---

## Documentation

The repository documentation is considered part of the project architecture.

Documentation is organised into independent sections:

* formats/
* data_dictionary/
* research/
* findings/
* examples/

The implementation should always follow the documented data model.

---

# Design Principles

PylonInsight follows the following principles:

* Open source
* Reproducible research
* Hardware-independent analysis
* Incremental imports
* Data integrity
* Separation between raw exports and normalized data
* Evidence-based reverse engineering

---

# Future Components

Planned future modules include:

* Web dashboard
* REST API
* Automatic report generation
* Statistical analysis
* Machine learning based anomaly detection
* Multi-installation comparison
* Plugin system
