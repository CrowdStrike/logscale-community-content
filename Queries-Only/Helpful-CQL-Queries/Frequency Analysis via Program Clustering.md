```
// Get file names of interest
event_platform=Win #event_simpleName=ProcessRollup2 FileName=/(whoami|arp|cmd|net|net1|ipconfig|route|netstat|nslookup|nltest|systeminfo|wmic|tasklist|tracert|ping|adfind|nbtstat|find|ldifde|netsh|wbadmin)\.exe/i

// Aggregate in 10 minute buckets; set search to 24 hours
| bucket(span=10min, field=[cid, aid, ComputerName,ParentBaseFileName,ParentProcessId], function=[count(FileName, distinct=true, as=fNameCount), collect([FileName, CommandLine])], limit=500)

// Set threshold at three distinct file name values
| test(fNameCount>=3)
```