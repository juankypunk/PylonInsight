# XHB BMU History Field Dictionary

This document describes the fields found in the `history.csv` files exported by BatteryView 3.9.4 for second-generation Pylontech XHB BMU boards (`V30R02C002`).

---

| CSV Column | Canonical Name                        | Type     | Unit | Description                                                                                 | Confidence    |
| ---------- | ------------------------------------- | -------- | ---- | ------------------------------------------------------------------------------------------- | ------------- |
| Item       | `record_index`                        | Integer  | -    | Sequential row number inside the exported history buffer. Not persistent between exports.   | ✅ Confirmed   |
| Time       | `timestamp`                           | DateTime | -    | Timestamp of the historical record. Natural identifier for incremental imports.             | ✅ Confirmed   |
| Vo(mV)     | `module_voltage`                      | Integer  | mV   | Total voltage of the battery module.                                                        | ✅ Confirmed   |
| Tmpr       | `module_temperature`                  | Integer  | ?    | Temperature-related value. Exact meaning under investigation.                               | 🔵 Hypothesis |
| BTlow      | `battery_temperature_low`             | Integer  | ?    | Lower battery temperature value or threshold.                                               | 🔵 Hypothesis |
| BThigh     | `battery_temperature_high`            | Integer  | ?    | Upper battery temperature value or threshold.                                               | 🔵 Hypothesis |
| BVlow      | `cell_voltage_low`                    | Integer  | mV   | Lowest cell voltage recorded within the module.                                             | 🟡 Likely     |
| BVhigh     | `cell_voltage_high`                   | Integer  | mV   | Highest cell voltage recorded within the module.                                            | 🟡 Likely     |
| PT.Tmpr    | `positive_terminal_temperature`       | Integer  | ?    | Temperature measured near the positive power terminal. Interpretation pending confirmation. | 🔵 Hypothesis |
| NT.Tmpr    | `negative_terminal_temperature`       | Integer  | ?    | Temperature measured near the negative power terminal. Interpretation pending confirmation. | 🔵 Hypothesis |
| Ref.Vol    | `reference_voltage`                   | Integer  | mV   | Internal reference voltage. Exact purpose unknown.                                          | 🔵 Hypothesis |
| Fan.Pwm    | `fan_pwm`                             | Integer  | %    | PWM duty cycle applied to the cooling fan. Observed value is always zero on H48050 modules. | 🟡 Likely     |
| Fan1.Rpm   | `fan1_rpm`                            | Integer  | rpm  | Fan 1 rotational speed. Observed value is always zero on H48050 modules.                    | 🟡 Likely     |
| Fan2.Rpm   | `fan2_rpm`                            | Integer  | rpm  | Fan 2 rotational speed. Observed value is always zero on H48050 modules.                    | 🟡 Likely     |
| Base.St    | `base_state`                          | String   | -    | BMU operating state (`Charge`, `Dischg`, `Idle`).                                           | 🟡 Likely     |
| Volt.St    | `voltage_state`                       | String   | -    | Voltage status (observed value: `Normal`).                                                  | 🟡 Likely     |
| Tmpr.St    | `temperature_state`                   | String   | -    | Internal temperature status.                                                                | 🟡 Likely     |
| PT.Tmpr.St | `positive_terminal_temperature_state` | String   | -    | Positive terminal temperature status.                                                       | 🔵 Hypothesis |
| NT.Tmpr.St | `negative_terminal_temperature_state` | String   | -    | Negative terminal temperature status.                                                       | 🔵 Hypothesis |
| Err.Code   | `error_code`                          | String   | Hex  | Error code reported by the BMU. Observed value: `0x0`.                                      | 🟡 Likely     |
| Events     | `events`                              | String   | -    | BMU event flags.                                                                            | ❓ Unknown     |

---

## Notes

* The timestamp is the recommended primary key for incremental imports.
* `Item` is only a positional index.
* Voltage values are stored in millivolts.
* The sampling interval declared in the CSV header (1800 s) does not match the observed interval between consecutive records.
* Fan-related fields are always zero on the analysed H48050 hardware and may be intended for other products using the same firmware family.
* Several temperature-related fields require further validation.
