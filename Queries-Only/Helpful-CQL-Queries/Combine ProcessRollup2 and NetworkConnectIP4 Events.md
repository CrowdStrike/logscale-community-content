```
(#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\chrome\.exe$/i) OR (#event_simpleName=NetworkConnectIP4 RemoteAddressIP4="8.8.8.8" event_platform=Win)
| falconPID:=TargetProcessId | falconPID:=ContextProcessId
| selfJoinFilter([aid, falconPID], where=[{#event_simpleName=ProcessRollup2}, {#event_simpleName=NetworkConnectIP4}], prefilter=true)
| groupBy([aid, falconPID], function=([collect([RemoteAddressIP4, ImageFileName, CommandLine]), count(#event_simpleName, distinct=true, as=eventCount)]))
| eventCount > 1
| drop([eventCount])
```