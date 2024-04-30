```
// Get file names of interest
event_platform=Win #event_simpleName=ProcessRollup2 FileName=/(whoami|arp|cmd|net|net1|ipconfig|route|netstat|nslookup|nltest|systeminfo|wmic|tasklist|tracert|ping|adfind|nbtstat|find|ldifde|netsh|wbadmin)\.exe/i

// Aggregate in 10 minute buckets; set search to 24 hours
| bucket(span=10min, field=[cid, aid, ComputerName,ParentBaseFileName,ParentProcessId], function=[count(FileName, distinct=true, as=fNameCount), collect([FileName, CommandLine])], limit=500)

// Set threshold at three distinct file name values
| test(fNameCount>=3)
```

Manually creating time shards without rounding to leverage groupBy:

```
// Get file names of interest
#event_simpleName=ProcessRollup2 event_platform=Win
| in(field="FileName", values=[whoami.exe, arp.exe, cmd.exe, net.exe, net1.exe, ipconfig.exe, route.exe, netstat.exe, nslookup.exe, nltest.exe, systeminfo.exe, wmic.exe, tasklist.exe, tracert.exe, ping.exe, adfind.exe, nbtstat.exe, find.exe, ldifde.exe, netsh.exe, wbadmin.exe], ignoreCase=true)

// Create time shards of 15 minutes
| regex(field=@timestamp, "(?<time_shard>[\d]{7})")
| format("%s000000", field=time_shard, as=time_shard)

// Group by shard and other key fields to emulate bucket
| groupBy([time_shard, cid, aid, ComputerName,ParentBaseFileName,ParentProcessId], function=[count(FileName, distinct=true, as=fNameCount), collect([FileName, CommandLine])], limit=max)

// Set threshold for file name appearances
| test(fNameCount>=4)

// Convert shard to human-redable format; shards will be slightly different as rounding is not occuring
| formatTime(format="%F %T", as="time_shard", field=time_shard)
```

Manually creating time shards with rounding to leverage groupBy:

```
// Get file names of interest
#event_simpleName=ProcessRollup2 event_platform=Win
| in(field="FileName", values=[whoami.exe, arp.exe, cmd.exe, net.exe, net1.exe, ipconfig.exe, route.exe, netstat.exe, nslookup.exe, nltest.exe, systeminfo.exe, wmic.exe, tasklist.exe, tracert.exe, ping.exe, adfind.exe, nbtstat.exe, find.exe, ldifde.exe, netsh.exe, wbadmin.exe], ignoreCase=true)

// Create time shards of 15 minutes
| rounddown := @timestamp % 900000
| bucket := @timestamp - rounddown

// Group by shard and other key fields to emulate bucket
| groupBy([bucket, aid, ComputerName, ParentBaseFileName, ParentProcessId], function=[count(FileName, distinct=true, as=fNameCount), collect([FileName, CommandLine])], limit=max)

// Set threshold for file name appearances
| test(fNameCount>=4)

// Convert shard to human-redable format
| formatTime(format="%F %T", as="bucket", field=bucket)
```