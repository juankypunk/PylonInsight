# Legacy BMU History CSV Format

## Scope

This document describes the `history.csv` file exported by **BatteryView 3.9.4** for the first-generation Pylontech BMU boards.

Validated hardware:

* Device name: `bmu`
* Board version: `HP0115SV10R01`
* Main software: `B52.2.0`
* Software version: `V3.2`

Field semantics are documented separately in:

```text
docs/data_dictionary/history_bmu_fields.md
```

---

# File Structure

A BMU history export consists of four sections.

```text
+----------------------------+
| Header (4 lines)           |
+----------------------------+
| Column names (1 line)      |
+----------------------------+
| Data records               |
+----------------------------+
| Footer (2 lines)           |
+----------------------------+
```

The file is encoded as CSV using comma-separated values.

---

# Header

Example:

```text
Save,data,every,1800,S
```

The header declares a nominal sampling interval of **1800 seconds**.

Current observations indicate that the effective sampling interval matches the declared value for this hardware generation.

---

# Column Header

Observed columns:

```text
Item,
Time,
Vo(mV),
Tempr,
Tlow,
Thigh,
Vlowest,
Vhighest,
Volt.St,
Temp.St,
Events,
BatEvents
```

The meaning of every field is documented in:

```text
docs/data_dictionary/history_bmu_fields.md
```

---

# Data Records

Each record represents one historical snapshot stored by the BMU.

Observed characteristics:

* Records are ordered chronologically.
* Sampling interval is approximately 1800 seconds.
* Timestamp resolution is one second.

The timestamp should be considered the natural identifier of a history record.

The `Item` field is only a sequential row number and must not be used as a persistent identifier.

---

# Footer

Observed footer:

```text
Command,completed,successfully
$$
```

These lines are not part of the dataset and should be ignored by parsers.

---

# Format Invariants

| Property                            | Status    |
| ----------------------------------- | --------- |
| CSV format                          | Confirmed |
| Header length = 4 lines             | Confirmed |
| Footer length = 2 lines             | Confirmed |
| Chronological ordering              | Confirmed |
| Nominal sampling interval = 1800 s  | Confirmed |
| Effective sampling interval ≈1800 s | Confirmed |

---

# Parsing Recommendations

A parser should:

* Ignore the header.
* Read the column definition.
* Import every data record.
* Ignore the footer.
* Use the timestamp for incremental imports.
* Ignore the `Item` field for database keys.

---

# Related Documentation

* `docs/data_dictionary/history_bmu_fields.md`
* `docs/findings.md`
