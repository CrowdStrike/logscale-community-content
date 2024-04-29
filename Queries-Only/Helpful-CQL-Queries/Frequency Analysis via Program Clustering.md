```
// Get file names of interest
event_platform=Win #event_simpleName=ProcessRollup2 FileName=/(whoami|arp|cmd|net|net1|ipconfig|route|netstat|nslookup|nltest|systeminfo|wmic|tasklist|tracert|ping|adfind|nbtstat|find|ldifde|netsh|wbadmin)\.exe/i

// Aggregate by system and lineage
| groupBy([cid, aid, ComputerName,ParentBaseFileName,ParentProcessId], function=([count(FileName, distinct=true, as=fNameCount), collect([FileName, CommandLine]), min(@timestamp), max(@timestamp)]))

// Check for at least three occurances of files of interest
| test(fNameCount>3)

// Calculate time deltas
| TimeDelta:=(_max-_min)
| TimeDeltaMin:=TimeDelta/1000/60

// Set cluster time to 10 minutes or fewer
| test(TimeDeltaMin<=10)

// Make duration field human readable
| formatDuration(TimeDelta, as=TimeDelta, precision=2)

// Organize output as a table
| table([cid, aid, ComputerName,ParentBaseFileName,ParentProcessId, fNameCount, TimeDelta, FileName, CommandLine], limit=20000)
```