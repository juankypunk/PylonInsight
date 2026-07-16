# SC0500A BMS Event Field Dictionary

This document describes the fields present in `event.csv` exported by BatteryView 3.9.4 from the SC0500A BMS.

---

| CSV Column | Canonical Name             | Type       | Unit     | Description                                                                                  | Confidence    |
| ---------- | -------------------------- | ---------- | -------- | -------------------------------------------------------------------------------------------- | ------------- |
| Item       | `record_index`             | Integer    | -        | Sequential row number within the exported event log. Not persistent.                         | ✅ Confirmed   |
| Date       | `record_date`              | Date       | YY-MM-DD | Date portion of the event timestamp.                                                         | ✅ Confirmed   |
| Time       | `record_time`              | Time       | HH:MM:SS | Time portion of the event timestamp.                                                         | ✅ Confirmed   |
| Vo(mV)     | `pack_voltage`             | Integer    | mV       | Total battery pack voltage.                                                                  | ✅ Confirmed   |
| Cu(mA)     | `pack_current`             | Integer    | mA       | Battery current. Positive and negative values indicate charging or discharging.              | 🟡 Likely     |
| Tempr      | `temperature`              | Integer    | ?        | Internal temperature-related value. Scaling under investigation.                             | 🔵 Hypothesis |
| BTlow      | `battery_temperature_low`  | Integer    | ?        | Lowest battery temperature value or threshold.                                               | 🔵 Hypothesis |
| BThigh     | `battery_temperature_high` | Integer    | ?        | Highest battery temperature value or threshold.                                              | 🔵 Hypothesis |
| BVlow      | `battery_voltage_low`      | Integer    | mV       | Lowest battery voltage measured.                                                             | 🟡 Likely     |
| BVhigh     | `battery_voltage_high`     | Integer    | mV       | Highest battery voltage measured.                                                            | 🟡 Likely     |
| UTlow      | `unit_temperature_low`     | Integer    | ?        | Lowest unit temperature value or threshold.                                                  | 🔵 Hypothesis |
| UThigh     | `unit_temperature_high`    | Integer    | ?        | Highest unit temperature value or threshold.                                                 | 🔵 Hypothesis |
| UVlow      | `unit_voltage_low`         | Integer    | mV       | Lowest unit voltage measured.                                                                | 🟡 Likely     |
| UVhigh     | `unit_voltage_high`        | Integer    | mV       | Highest unit voltage measured.                                                               | 🟡 Likely     |
| Base.St    | `base_state`               | String     | -        | Operating state (Charge, Dischg, Idle).                                                      | 🟡 Likely     |
| Volt.St    | `voltage_state`            | String     | -        | Voltage status.                                                                              | 🟡 Likely     |
| Curr.St    | `current_state`            | String     | -        | Current status.                                                                              | 🟡 Likely     |
| Temp.St    | `temperature_state`        | String     | -        | Temperature status.                                                                          | 🟡 Likely     |
| Per%       | `state_of_charge`          | Percentage | %        | Battery State of Charge (SOC).                                                               | ✅ Confirmed   |
| ErrCode    | `error_code`               | String     | Hex      | Error code reported by the BMS (e.g. `0x0`).                                                 | 🟡 Likely     |
| Events     | `event_flags`              | String     | -        | Event code(s) describing the condition that triggered the record (e.g. `BHV`, `BLV`, `DSG`). | 🟡 Likely     |
| BatEvents  | `battery_event_flags`      | String     | -        | Battery-level event flags. Exact semantics under investigation.                              | ❓ Unknown     |
| UnitEvents | `unit_event_flags`         | String     | -        | Module/unit event flags. Exact semantics under investigation.                                | ❓ Unknown     |

---

## Notes

* The event timestamp is reconstructed by combining the `Date` and `Time` columns.
* `Item` is only a sequential index and must not be used as a persistent identifier.
* Each record represents the complete BMS operating state when an event occurred.
* Event codes (`Events`) are currently being reverse engineered and should not yet be interpreted as fault codes.
* The CSV structure is closely related to `history.csv`, but records are generated on an event basis rather than at fixed time intervals.
