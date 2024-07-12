```
// Get SensorHeartbeat events for Windows, macOS, and Linux
#event_simpleName=SensorHeartbeat event_platform=/(^(Win|Mac|Lin)$)/
// Get most recent event for each aid value and include event_platform
| groupBy([event_platform, aid], function=([selectFromMax(field="@timestamp", include=[SensorStateBitMap])]))
// Aggregate by event_platform and count by SensorStateBitMap
| groupBy(event_platform, function=([{SensorStateBitMap=2 | count(as=RFM) }, {SensorStateBitMap=0 | count(as=OK)}])) 
// Create total and percentage values
| Total:= RFM + OK | PercentRFM := (RFM / Total) * 100 
// Optional: set threshold for % of systems in RFM; uncomment if desired
// | PercentRFM > 5
// Format percentage value
| PercentRFM:= format(format="%,.2f%%", field=[PercentRFM])
// Order fields with table
| table([event_platform, Total, RFM, OK, PercentRFM])
```