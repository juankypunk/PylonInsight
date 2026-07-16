# Legacy BMU Event Field Dictionary

This document describes the fields present in `event.csv` exported by BatteryView 3.9.4 from first-generation Pylontech BMUs.

## Notes

BatteryView omits the **Date** column from the exported CSV header.

The logical data model is:

```text
Item
Date
Time
Vo(mV)
Tempr
Tlow
Thigh
Vlowest
Vhighest
Volt.St
Temp.St
Events
BatEvents
```

The timestamp is reconstructed by combining **Date** and **Time**.

---

| CSV Column       | Canonical Name         | Type    | Unit     | Description                                                                            | Confidence    |
| ---------------- | ---------------------- | ------- | -------- | -------------------------------------------------------------------------------------- | ------------- |
| Item             | `record_index`         | Integer | -        | Sequential row number within the exported event log. Not persistent.                   | ✅ Confirmed   |
| Date *(logical)* | `record_date`          | Date    | YY-MM-DD | Date portion of the event timestamp. Missing from exported header.                     | ✅ Confirmed   |
| Time             | `record_time`          | Time    | HH:MM:SS | Time portion of the event timestamp.                                                   | ✅ Confirmed   |
| Vo(mV)           | `module_voltage`       | Integer | mV       | Module output voltage.                                                                 | ✅ Confirmed   |
| Tempr            | `module_temperature`   | Integer | ?        | Internal module temperature. Scaling under investigation.                              | 🟡 Likely     |
| Tlow             | `lowest_temperature`   | Integer | ?        | Lowest measured temperature or configured threshold.                                   | 🔵 Hypothesis |
| Thigh            | `highest_temperature`  | Integer | ?        | Highest measured temperature or configured threshold.                                  | 🔵 Hypothesis |
| Vlowest          | `lowest_cell_voltage`  | Integer | mV       | Lowest measured cell voltage.                                                          | 🟡 Likely     |
| Vhighest         | `highest_cell_voltage` | Integer | mV       | Highest measured cell voltage.                                                         | 🟡 Likely     |
| Volt.St          | `voltage_state`        | String  | -        | Voltage status reported by the BMU.                                                    | 🟡 Likely     |
| Temp.St          | `temperature_state`    | String  | -        | Temperature status reported by the BMU.                                                | 🟡 Likely     |
| Events           | `event_flags`          | String  | -        | Event code(s) associated with this record (e.g. BHV, BVNOR, PHV, PVNOR, IDLE, SYSERR). | 🟡 Likely     |
| BatEvents        | `battery_event_flags`  | String  | -        | Additional battery-level event flags. Exact semantics under investigation.             | ❓ Unknown     |

---

## Notes

* The natural key is (`Date`, `Time`).
* `Item` is only a sequential index within the exported file.
* Event records represent snapshots generated when an event occurs.
* Event codes are currently documented in `research/event_code_reverse_engineering.md`.
* Additional event codes may appear in future firmware versions.
