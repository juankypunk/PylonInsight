# BMS History Field Dictionary

This document describes the fields found in the `history.csv` files exported by BatteryView 3.9.4 for the Pylontech SC0500A BMS.

---

| CSV Column | Canonical Name         | Type    | Unit     | Description                                                                                                                                         | Confidence    |
| ---------- | ---------------------- | ------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Item       | `record_index`         | Integer | -        | Sequential row number inside the exported FIFO buffer (0–511). This value is not persistent between exports and must not be used as a database key. | ✅ Confirmed   |
| Date       | `record_date`          | Date    | YY-MM-DD | Date portion of the timestamp.                                                                                                                      | ✅ Confirmed   |
| Time       | `record_time`          | Time    | HH:MM:SS | Time portion of the timestamp. Together with `Date` forms the record timestamp.                                                                     | ✅ Confirmed   |
| Vo(mV)     | `stack_voltage`        | Integer | mV       | Total voltage of the complete battery stack.                                                                                                        | ✅ Confirmed   |
| Cu(mA)     | `stack_current`        | Integer | mA       | Battery current. Positive values correspond to charging, negative values to discharging.                                                            | ✅ Confirmed   |
| Tempr      | `temperature`          | Integer | ?        | Temperature-related field. Exact meaning still under investigation.                                                                                 | 🔵 Hypothesis |
| BTlow      | `battery_temp_low`     | Integer | ?        | Lower battery temperature value or threshold. Appears to be stored using a scaled integer representation.                                           | 🔵 Hypothesis |
| BThigh     | `battery_temp_high`    | Integer | ?        | Upper battery temperature value or threshold. Appears to be stored using a scaled integer representation.                                           | 🔵 Hypothesis |
| BVlow      | `battery_voltage_low`  | Integer | ?        | Battery voltage related field. Exact meaning not yet confirmed.                                                                                     | ❓ Unknown     |
| BVhigh     | `battery_voltage_high` | Integer | ?        | Battery voltage related field. Values suggest cell-level voltage (≈3.2–3.6 V after scaling).                                                        | 🟡 Likely     |
| UTlow      | `unit_temp_low`        | Integer | ?        | Unknown.                                                                                                                                            | ❓ Unknown     |
| UThigh     | `unit_temp_high`       | Integer | ?        | Unknown.                                                                                                                                            | ❓ Unknown     |
| UVlow      | `unit_voltage_low`     | Integer | ?        | Voltage-related field. Values suggest module-level voltage (≈48–53 V after scaling).                                                                | 🟡 Likely     |
| UVhigh     | `unit_voltage_high`    | Integer | ?        | Voltage-related field. Values suggest module-level voltage (≈48–53 V after scaling).                                                                | 🟡 Likely     |
| Base.St    | `base_state`           | String  | -        | Main operating state (`Idle`, `Charge`, `Dischg`).                                                                                                  | ✅ Confirmed   |
| Volt.St    | `voltage_state`        | String  | -        | Voltage status reported by the BMS (observed: `Normal`).                                                                                            | 🟡 Likely     |
| Curr.St    | `current_state`        | String  | -        | Current status reported by the BMS (observed: `Normal`).                                                                                            | 🟡 Likely     |
| Temp.St    | `temperature_state`    | String  | -        | Temperature status reported by the BMS (observed: `Normal`).                                                                                        | 🟡 Likely     |
| Per%       | `state_of_charge`      | Integer | %        | Battery State of Charge (SOC).                                                                                                                      | ✅ Confirmed   |
| ErrCode    | `error_code`           | String  | Hex      | BMS error code (observed value: `0x0`).                                                                                                             | 🟡 Likely     |
| Events     | `events`               | String  | -        | System event flags (e.g. `CHG`).                                                                                                                    | 🟡 Likely     |
| BatEvents  | `battery_events`       | String  | -        | Battery-specific event flags. Meaning under investigation.                                                                                          | ❓ Unknown     |
| UnitEvents | `unit_events`          | String  | -        | Module-specific event flags. Meaning under investigation.                                                                                           | ❓ Unknown     |

---

## Notes

* The natural identifier of a history record is the reconstructed timestamp (`Date` + `Time`).
* The `Item` field is only a positional index within the FIFO buffer.
* Several fields (`BT*`, `BV*`, `UT*`, `UV*`) require further validation by comparison with BMU history exports.
* Field names are intended to be stable identifiers used by PylonInsight and may differ from future interpretations of the underlying BatteryView terminology.
