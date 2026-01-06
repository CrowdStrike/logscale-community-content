```
// Get all sensor heartbeat events
#event_simpleName=SensorHeartbeat

// Get last event for each Agent ID value
| groupBy([aid], function=([selectLast([@timestamp])]))

// Create offlineTime_m field that represents the number of minutes since last heartbeat event; round this numbner
| offlineTime_m:=(now()-@timestamp)/1000/60 | round("offlineTime_m")

// Create offlineDuration field that shows offlineTime_m in a human-readable duration with a precision of 2
| offlineDuration:=formatDuration("offlineTime_m", precision=2, from=m)

// Check to see if it has been at least 20 minutes since last heartbeat event was seen (note: heartbeats are typically sent every 2 minutes)
| test(offlineTime_m>20)

// Add host details from AID Master
| aid=~match(file="aid_master_main.csv", column=[aid], strict=false)
```

[Reference](https://www.reddit.com/r/crowdstrike/comments/1q4vl2l/alerting_based_on_missing_heartbeats/)
