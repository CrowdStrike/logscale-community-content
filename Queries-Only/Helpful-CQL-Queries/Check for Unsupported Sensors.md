```
// Get OsVersionInfo events
#event_simpleName=OsVersionInfo
// Get latest OsVersionInfo data per aid
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[event_platform, ComputerName, AgentVersion])]), limit=max)
// Extract Falcon build number from AgentVersion 
| AgentVersion=/\d+\.\d+\.(?<BUILD>\d+)\./
// Bring in sensor support details from lookup file
| BUILD=~match(file="falcon/investigate/sensors_support_info.csv", column="BUILD", include=[SUPPORT_ENDS], strict=true)
// Aggregate support status by Falcon build
| groupBy([event_platform, BUILD, AgentVersion, SUPPORT_ENDS], function=([count(aid, as=TotalSystems)]))
// Parse timestamp into epoch
| parseTimestamp("M/d/yy",field=SUPPORT_ENDS, as=SUPPORT_ENDS_EPOCH, timezone="UTC")
// See what sensors are out of support
| test(SUPPORT_ENDS_EPOCH < now())
// Drop unnecessary fields
| drop([@timezone, SUPPORT_ENDS_EPOCH, SUPPORT_ENDS_EPOCH.nanos])
```