| Status           | Meaning                                                        |
| ----------------- | --------------------------------------------------------------------- |
| ✅ **Confirmed**   | Verified experimentally using one or more acquisition campaigns.      |
| 🟡 **Likely**     | Strong evidence exists, but additional validation is still desirable. |
| 🔵 **Hypothesis** | Plausible explanation that has not yet been experimentally verified.  |
| ❌ **Rejected**    | Hypothesis disproved by subsequent observations.                      |



## F-001 — BMS history sampling interval ##

**Status:** ✅ Confirmed

**Finding**

The SC0500A BMS stores one history record every 1800 seconds (30 minutes).

**Evidence**
- history.csv header contains: 'Save,data,every,1800,S'
- Consecutive timestamps are separated by approximately 30 minutes.

**Confidence**

Confirmed


## F-002 — BMS history records are immutable ##

**Status:** ✅ Confirmed

**Finding**

Once written, a BMS history record is never modified.

**Evidence**

The same timestamps extracted from different acquisition campaigns contain identical values.

**Implications**

Incremental imports are safe.


## F-003 — BMS history uses a circular FIFO buffer ##

**Status:** ✅ Confirmed

**Finding**

The BMS stores its history in a fixed-size FIFO circular buffer.

**Evidence**

- Older records disappear while newer records are appended.

- The exported file always contains the most recent history.

**Confidence**

Confirmed


## F-004 — BMS history buffer capacity ##

**Status:** ✅ Confirmed

**Finding**

The BMS history buffer stores 512 records.

**Evidence**

Each exported history.csv contains:

- 4 header rows
- 512 data rows
- 2 footer rows

The covered time span matches:

- 511 × 1800 s
- ≈ 10 days 15 h 30 min

**Implications**

Users should perform acquisitions at least every 10 days to avoid losing historical data.

A weekly acquisition is recommended.


## F-005 — Timestamp is a candidate primary key for BMS history ##

**Status:** 🟡 Likely

**Finding**

The timestamp appears to uniquely identify each BMS history record.

**Evidence**

- Identical timestamps found in different campaigns contain identical values.

- No duplicate timestamps have been observed.

- Remaining work

- Verify uniqueness over a larger dataset.


## F-006 — Incremental import is feasible ##

**Status:** ✅ Confirmed

**Finding**

BMS history can be imported incrementally.

**Evidence**

Historical records are immutable and duplicated across acquisitions.

* Proposed implementation
INSERT ...
ON CONFLICT DO NOTHING;


## F-007 — Module history format differs from BMS history ##

**Status:** ✅ Confirmed

**Finding**

Module history.csv files do not follow exactly the same structure as the BMS history.

**Evidence**

- Different record counts have been observed.

- The temporal behaviour also differs from the BMS history.

**Implications**

Independent parsers should be implemented.


## F-008 — Two BMU hardware generations identified ##

**Status:** ✅ Confirmed

**Finding**

Two different BMU hardware/firmware platforms are present in the same PowerCube X1.

Generation 1
Device name     : bmu
Board           : HP0115SV10R01
Main FW         : B52.2.0
Soft            : V3.2
Boot            : V1.4
Release         : 2021-09-29

Generation 2
Device name     : XHB_BMU_NT
Board           : V30R02C002
Main FW         : B52.5.0
Soft            : V1.2
Boot            : V1.0
Release         : 2025-10-20
AFE             : LTC6813
Evidence

Batt2 (replacement module) differs completely from Batt1 and Batt3.


## F-009 — Batt1 export consistently reports a non-fatal error ##

**Status:** 🟡 Likely

**Finding**

Batt1 always finishes the history export with:

Error!
Invalid command or fail to execute.

**Evidence**

- The behaviour is reproducible.

- Exported data are complete and internally consistent.

- No anomalies have been detected in the history records.

**Hypothesis**

The error is probably triggered by a non-critical command executed after the history transfer has completed.


## F-010 — Metadata are distributed across multiple export files ##

**Status:** ✅ Confirmed

**Finding**

BatteryView distributes device metadata across different exported files.

**Evidence**

Firmware information, board versions, boot versions, serial numbers, barcodes and manufacturing information are located mainly in the *_detailed.txt files.

**Implications**

The *_detailed.txt files should be parsed and stored.

Discarding them would result in the loss of valuable device metadata.


## F-011 — Device metadata are suitable for inventory tracking ##

**Status:** 🟡 Likely

**Finding**

Static metadata change very rarely compared with history and event data.

**Implications**

The database should distinguish between:

- Device inventory
- Acquisition campaigns
- Dynamic measurements

This avoids unnecessary duplication while preserving firmware evolution over time.

## F-012 — Advertised sampling interval may differ from effective sampling interval ##

**Status:** 🟡 Likely

**Finding**

The sampling interval declared in the CSV header (Save,data,every,1800,S) does not necessarily match the effective interval between consecutive history records.

**Evidence**

* SC0500A BMS: advertised 1800 s, observed ≈1800 s.
* Legacy BMU: advertised 1800 s, observed ≈1800 s (según tus observaciones anteriores).
* XHB BMU: advertised 1800 s, observed ≈420 s (≈7 min), based on timestamp analysis.

**Implications**

Software must derive the effective sampling interval from the timestamps instead of assuming the value declared in the header.