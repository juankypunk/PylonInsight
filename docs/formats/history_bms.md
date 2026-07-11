# BMS History CSV Format

## Scope

This document describes the `history.csv` file exported by **BatteryView 3.9.4** for the **Pylontech SC0500A Battery Management System (BMS)**.

The purpose of this document is to define the file structure and format independently of any software implementation. Field semantics are documented separately in `docs/data_dictionary/history_bms_fields.md`.

---

# File Structure

A BMS history export consists of four sections:

```
+----------------------------+
| Header (4 lines)           |
+----------------------------+
| Column names (1 line)      |
+----------------------------+
| Data records (512 lines)   |
+----------------------------+
| Footer (2 lines)           |
+----------------------------+
```

The file is encoded as CSV using comma-separated values.

---

# Header

The header contains acquisition metadata.

Example:

```
Save,data,every,1800,S
```

### Observations

* Sampling interval: **1800 seconds**
* Sampling period: **30 minutes**
* The sampling interval is constant in all analysed campaigns.

---

# Column Header

The first line after the header defines the record structure.

Example:

```
Item,Time,Vo(mV),Cu(mA),Tempr,...
```

The complete description of every field is available in:

```
docs/data_dictionary/history_bms_fields.md
```

---

# Data Records

Each record represents one historical snapshot stored by the BMS.

Observed properties:

* Exactly **512 records** are exported.
* Records are ordered chronologically.
* Timestamp resolution is one second.
* Sampling interval is nominally 1800 seconds.
* Records are immutable once stored.

The timestamp should be considered the natural identifier of a history record.

The `Item` column is only a positional index inside the exported FIFO buffer and **must not** be used as a persistent identifier.

---

# Footer

Current BatteryView versions terminate the file with:

```
Command,completed,successfully
$$
```

These lines are not part of the dataset and should be ignored during parsing.

---

# Format Invariants

The following characteristics have been confirmed experimentally.

| Property                                  | Status    |
| ----------------------------------------- | --------- |
| Header length = 4 lines                   | Confirmed |
| Footer length = 2 lines                   | Confirmed |
| History records = 512                     | Confirmed |
| Sampling interval = 1800 s                | Confirmed |
| FIFO circular buffer                      | Confirmed |
| Records are immutable                     | Confirmed |
| Chronological ordering                    | Confirmed |
| Timestamp suitable for incremental import | Confirmed |

---

# Parsing Recommendations

A parser should:

* Ignore the header.
* Read the column definition.
* Import every data record.
* Ignore the footer.
* Use the timestamp to detect duplicated records.
* Treat the `Item` field only as a transient row number.

---

# Database Recommendations

For incremental imports, the timestamp should be used as the primary candidate key.

Example:

```
PRIMARY KEY (timestamp)
```

or

```
INSERT ... ON CONFLICT DO NOTHING
```

depending on the database design.

---

# Related Documentation

* `docs/data_dictionary/history_bms_fields.md`
* `docs/findings.md`
