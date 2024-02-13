```
event_type=ZeroTrustHostAssessment
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[scores.os, scores.sensor, scores.overall])]))
| join(query={#data_source_name=aidmaster }, field=[aid], include=[ComputerName, event_platform])
```