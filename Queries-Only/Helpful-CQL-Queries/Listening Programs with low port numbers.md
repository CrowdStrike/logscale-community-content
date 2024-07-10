```
// Get Windows events where a program is listening on a port under 10000 and all process execution events
event_platform=Win (#event_simpleName=NetworkListenIP4 LocalPort<10000) OR (#event_simpleName=ProcessRollup2)
// Normalize UPID
| falconPID:= TargetProcessId | falconPID:=ContextProcessId
// Use selfJoinFilter to make sure both events occured under an aid/UPID pair
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=NetworkListenIP4}, {#event_simpleName=ProcessRollup2}])
// Aggregate results
| groupBy([aid, ComputerName, falconPID], function=([collect([UserSid, UserName, ImageFileName, LocalPort, Protocol])]))
// Merge data from aid_master_main
| match(file="aid_master_main.csv", field=[aid], column=aid, include=[ProductType, Version])
// Use Falcon Helper to change decimal values to human-readable values
| $falcon/helper:enrich(field=ProductType)
| $falcon/helper:enrich(field=Protocol)
```