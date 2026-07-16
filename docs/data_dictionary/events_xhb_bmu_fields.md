# XHB_BMU_NT Event Field Dictionary

This document describes the fields present in `event.csv` exported by BatteryView 3.9.4 from XHB_BMU_NT modules.

## Notes

BatteryView omits the **Date** column from the exported CSV header.

The logical data model is:

```text
Item
Date
Time
Vo(mV)
Tmpr
BTlow
BThigh
BVlow
BVhigh
PT.Tmpr
NT.Tmpr
Ref.Vol
Fan.Pwm
Fan1.Rpm
Fan2.Rpm
Base.St
Volt.St
Tmpr.St
PT.Tmpr.St
NT.Tmpr.St
Err.Code
Events
```

The timestamp is reconstructed by combining **Date** and **Time**.

---

| CSV Column       | Canonical Name              | Type    | Unit     | Description                                                                                                        | Confidence    |
| ---------------- | --------------------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------ | ------------- |
| Item             | `record_index`              | Integer | -        | Sequential row number within the exported event log. Not persistent.                                               | ✅ Confirmed   |
| Date *(logical)* | `record_date`               | Date    | YY-MM-DD | Date portion of the event timestamp. Missing from exported header.                                                 | ✅ Confirmed   |
| Time             | `record_time`               | Time    | HH:MM:SS | Time portion of the event timestamp.                                                                               | ✅ Confirmed   |
| Vo(mV)           | `module_voltage`            | Integer | mV       | Module output voltage.                                                                                             | ✅ Confirmed   |
| Tmpr             | `module_temperature`        | Integer | ?        | Main module temperature. Scaling under investigation.                                                              | 🟡 Likely     |
| BTlow            | `battery_temperature_low`   | Integer | ?        | Lowest battery temperature or threshold.                                                                           | 🔵 Hypothesis |
| BThigh           | `battery_temperature_high`  | Integer | ?        | Highest battery temperature or threshold.                                                                          | 🔵 Hypothesis |
| BVlow            | `lowest_cell_voltage`       | Integer | mV       | Lowest measured cell voltage.                                                                                      | 🟡 Likely     |
| BVhigh           | `highest_cell_voltage`      | Integer | mV       | Highest measured cell voltage.                                                                                     | 🟡 Likely     |
| PT.Tmpr          | `power_temperature`         | Integer | ?        | Additional temperature sensor (Power section). Exact location under investigation.                                 | 🔵 Hypothesis |
| NT.Tmpr          | `ambient_temperature`       | Integer | ?        | Additional temperature sensor. Exact location under investigation.                                                 | 🔵 Hypothesis |
| Ref.Vol          | `reference_voltage`         | Integer | mV       | Internal reference voltage used by the BMU.                                                                        | 🔵 Hypothesis |
| Fan.Pwm          | `fan_pwm`                   | Integer | %        | PWM command sent to the cooling fan. Zero on fanless modules.                                                      | 🟡 Likely     |
| Fan1.Rpm         | `fan1_speed`                | Integer | rpm      | Fan 1 rotational speed.                                                                                            | 🟡 Likely     |
| Fan2.Rpm         | `fan2_speed`                | Integer | rpm      | Fan 2 rotational speed.                                                                                            | 🟡 Likely     |
| Base.St          | `base_state`                | String  | -        | Operating state (Idle, Charge, Dischg, etc.).                                                                      | 🟡 Likely     |
| Volt.St          | `voltage_state`             | String  | -        | Voltage status.                                                                                                    | 🟡 Likely     |
| Tmpr.St          | `temperature_state`         | String  | -        | General temperature status.                                                                                        | 🟡 Likely     |
| PT.Tmpr.St       | `power_temperature_state`   | String  | -        | Status associated with PT.Tmpr.                                                                                    | 🔵 Hypothesis |
| NT.Tmpr.St       | `ambient_temperature_state` | String  | -        | Status associated with NT.Tmpr.                                                                                    | 🔵 Hypothesis |
| Err.Code         | `error_code`                | String  | Hex      | Error code reported by the BMU (e.g. `0x0`).                                                                       | 🟡 Likely     |
| Events           | `event_flags`               | String  | -        | Event code(s) associated with this record (e.g. BHV). Additional codes expected as more datasets become available. | 🟡 Likely     |

---

## Notes

* The natural key is (`Date`, `Time`).
* `Item` is only a sequential index within the exported file.
* Event records are generated when the BMU records a state transition or significant event.
* The XHB generation provides additional telemetry compared with the legacy BMU.
* Several fields remain under investigation and will be updated as more datasets become available.
