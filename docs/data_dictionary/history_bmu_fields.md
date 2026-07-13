# Legacy BMU History Field Dictionary

This document describes the fields found in the `history.csv` files exported by BatteryView 3.9.4 for first-generation Pylontech BMU boards (`HP0115SV10R01`).

---

| CSV Column | Canonical Name       | Type     | Unit | Description                                                                                                                      | Confidence    |
| ---------- | -------------------- | -------- | ---- | -------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Item       | `record_index`       | Integer  | -    | Sequential row number inside the exported history buffer. Not persistent between exports and must not be used as a database key. | ✅ Confirmed   |
| Date       | `record_date`        | Date | -    | Date portion of the timestamp.             | ✅ Confirmed   |
| Time       | `record_time`          | DateTime | -    | Timestamp of the historical record. Natural identifier for incremental imports.                                                  | ✅ Confirmed   |
| Vo(mV)     | `module_voltage`     | Integer  | mV   | Total voltage of the battery module.                                                                                             | ✅ Confirmed   |
| Tempr      | `module_temperature` | Integer  | ?    | Temperature-related value. Exact meaning under investigation.                                                                    | 🔵 Hypothesis |
| Tlow       | `temperature_low`    | Integer  | ?    | Lower temperature value or threshold.                                                                                            | 🔵 Hypothesis |
| Thigh      | `temperature_high`   | Integer  | ?    | Upper temperature value or threshold.                                                                                            | 🔵 Hypothesis |
| Vlowest    | `cell_voltage_low`   | Integer  | mV   | Lowest cell voltage recorded within the module.                                                                                  | 🟡 Likely     |
| Vhighest   | `cell_voltage_high`  | Integer  | mV   | Highest cell voltage recorded within the module.                                                                                 | 🟡 Likely     |
| Volt.St    | `voltage_state`      | String   | -    | Voltage status (observed value: `Normal`).                                                                                       | 🟡 Likely     |
| Temp.St    | `temperature_state`  | String   | -    | Temperature status (observed value: `Normal`).                                                                                   | 🟡 Likely     |
| Events     | `events`             | String   | -    | General BMU event flags.                                                                                                         | ❓ Unknown     |
| BatEvents  | `battery_events`     | String   | -    | Battery-specific event flags.                                                                                                    | ❓ Unknown     |

---

## Notes

- The natural identifier of a history record is the reconstructed timestamp (`Date` + `Time`).
- The parser should combine the `Date` and `Time` columns into a single `timestamp` value.
- The timestamp is the recommended primary key for incremental imports.
- `Item` is only a positional index within the history buffer and must not be used as a persistent identifier.
- Voltage fields are stored in millivolts.
- Temperature scaling remains under investigation.
- The exact semantics of event fields have not yet been determined.
