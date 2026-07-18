## Deletion Policy

PylonInsight is designed as a historical analysis platform. Core entities (campaign, device) are protected against deletion while dependent records (history, events, device_snapshot, environment) are automatically removed when their parent export is intentionally deleted.

| Relation                          | ON UPDATE | ON DELETE | Motivo                                                 |
| --------------------------------- | --------- | --------- | ------------------------------------------------------ |
| campaign → campaign_export        | CASCADE   | RESTRICT  | No borrar campañas con datos asociados                 |
| device → campaign_export          | CASCADE   | RESTRICT  | No borrar dispositivos con histórico                   |
| campaign_export → history_*       | CASCADE   | CASCADE   | Los registros dependen completamente de la exportación |
| campaign_export → event_*         | CASCADE   | CASCADE   | Igual que `history`                                    |
| campaign_export → device_snapshot | CASCADE   | CASCADE   | El snapshot pertenece a esa exportación                |
| campaign → environment            | CASCADE   | CASCADE   | El entorno sólo tiene sentido dentro de una campaña    |
