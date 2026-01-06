```
// Get uninstall and heartbeat events
#event_simpleName=AcUninstallConfirmation OR #event_simpleName=SensorHeartbeat

// Narrow dataset by Agent ID; check both events happen on a single system
| selfJoinFilter(field=[aid], where=[{#event_simpleName=AcUninstallConfirmation}, {#event_simpleName=SensorHeartbeat}])

// Create unique timestamp values
| case {
  #event_simpleName=AcUninstallConfirmation | uninstallTime:=@timestamp;
  #event_simpleName=SensorHeartbeat         | heartbeatTime:=@timestamp;
}

// Get last uninstallTime and heartbeatTime values in epoch for each Agent ID
| groupBy([aid], function=([selectLast([uninstallTime, heartbeatTime])]))

// Make sure an uninstall occurred (accounts for selfJoinFilter being probabilistic)
| uninstallTime=*

// See if uninstallTime is > last heartbeatTime
| test(uninstallTime>heartbeatTime)

// Merge in AID Master Data
| aid=~match(file="aid_master_main.csv", column=[aid])

// Perform second check against AID Master to make sure LastSeen is before uninstall
| case {
  test(Time>uninstallTime) | Details:="System could still be viable.";
  test(Time<uninstallTime) | Details:="System likely uninstalled.";
}

// Convert time stamp values
| uninstallTime:=formatTime(format="%F %T %Z", field="uninstallTime")
| heartbeatTime:=formatTime(format="%F %T %Z", field="heartbeatTime")
| heartbeatTime:=formatTime(format="%F %T %Z", field="heartbeatTime")
| FirstSeen:=formatTime(format="%F %T %Z", field="FirstSeen")
| LastSeen:=formatTime(format="%F %T %Z", field="Time") | drop([Time])
```

[Reference](https://www.reddit.com/r/crowdstrike/comments/1q4oyhj/falcon_uninstall_siem_rule/)