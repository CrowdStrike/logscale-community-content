```
aid=1e0afc34e9634710bfcd2f46d8564ab1 (#event_simpleName=ProcessRollup2 FileName="powershell.exe")
| select([aid, ComputerName, CommandLine])
| join(key=aid, field=aid, query={#repo=sensor_metadata}, include=([AgentVersion, BiosManufacturer, FalconGroupingTags]))
```