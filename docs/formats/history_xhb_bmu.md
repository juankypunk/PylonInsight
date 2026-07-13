# XHB BMU History CSV Format

## Scope

This document describes the `history.csv` file exported by **BatteryView 3.9.4** for the second-generation Pylontech XHB BMU boards.

Validated hardware:

* Device name: `XHB_BMU_NT`
* Board version: `V30R02C002`
* Main software: `B52.5.0`
* Software version: `V1.2`

Field semantics are documented separately in:

```text
docs/data_dictionary/history_xhb_bmu_fields.md
```

---

# File Structure

An XHB BMU history export consists of four sections.

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

Although the header declares a sampling interval of **1800 seconds**, timestamp analysis shows that the effective interval between consecutive records is approximately **7 minutes**.

This discrepancy is currently under investigation and should not be relied upon by software.

---

# Column Header

Observed columns:

```text
Item,
Time,
Vo(mV),
Tmpr,
BTlow,
BThigh,
BVlow,
BVhigh,
PT.Tmpr,
NT.Tmpr,
Ref.Vol,
Fan.Pwm,
Fan1.Rpm,
Fan2.Rpm,
Base.St,
Volt.St,
Tmpr.St,
PT.Tmpr.St,
NT.Tmpr.St,
Err.Code,
Events
```

The meaning of every field is documented in:

```text
docs/data_dictionary/history_xhb_bmu_fields.md
```

---

# Data Records

Each record represents one historical snapshot stored by the BMU.

Observed characteristics:

* Records are ordered chronologically.
* Timestamp resolution is one second.
* Effective sampling interval is approximately seven minutes.
* The interval declared in the CSV header does not match the observed interval.

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

| Property                                           | Status    |
| -------------------------------------------------- | --------- |
| CSV format                                         | Confirmed |
| Header length = 4 lines                            | Confirmed |
| Footer length = 2 lines                            | Confirmed |
| Chronological ordering                             | Confirmed |
| Header advertises 1800 s                           | Confirmed |
| Effective sampling interval ≈7 min                 | Confirmed |
| Advertised interval differs from observed interval | Confirmed |

---

# Known Differences from Legacy BMU

Compared with the first-generation BMU, the XHB format introduces:

* Terminal temperature measurements.
* Reference voltage.
* Fan control fields.
* Fan speed fields.
* Base operating state.
* Error code.
* Additional status fields.

The XHB format therefore provides a significantly richer dataset than the legacy BMU format.

---

# Parsing Recommendations

A parser should:

* Ignore the header.
* Read the column definition.
* Import every data record.
* Ignore the footer.
* Derive the effective sampling interval from timestamps instead of relying on the value declared in the header.
* Use the timestamp for incremental imports.
* Ignore the `Item` field for database keys.

---

# Related Documentation

* `docs/data_dictionary/history_xhb_bmu_fields.md`
* `docs/findings.md`
