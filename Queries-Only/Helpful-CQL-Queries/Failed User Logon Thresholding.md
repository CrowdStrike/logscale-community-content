```
// Get Windows UserLogonFailed events
event_platform=Win #event_simpleName=UserLogonFailed2

// This line is completely optional, but converts SubStatus to hex
| SubStatus_hex:=format(field=SubStatus, "%x") | SubStatus_hex:=upper(SubStatus_hex) | SubStatus_hex:=format(format="0x%s", field=[SubStatus_hex])

// Aggregate results
| groupBy([aid, ComputerName, UserName, LogonType, SubStatus_hex, SubStatus], function=([count(aid, as=FailCount), min(ContextTimeStamp, as=FirstLogonAttempt), max(ContextTimeStamp, as=LastLogonAttempt), collect([LocalAddressIP4, aip])]))

// Perform rate calculations
| firstLastDeltaHours:=((LastLogonAttempt-FirstLogonAttempt)/60/60) | round("firstLastDeltaHours")
| logonAttemptsPerHour:=(failCount/firstLastDeltaHours) | round("logonAttemptsPerHour")

// Convert timestamps from epoch to human
| FirstLogonAttempt:=formatTime(format="%F %T.%L", field="FirstLogonAttempt")
| LastLogonAttempt:=formatTime(format="%F %T.%L", field="LastLogonAttempt")

// Optional: set threshold for failed logins
| FailCount> 5

// Sort descending
| sort(FailCount, order=desc, limit=2000)

// Convert fields from decimal to human readable
| $falcon/helper:enrich(field=LogonType)
| $falcon/helper:enrich(field=SubStatus)
```