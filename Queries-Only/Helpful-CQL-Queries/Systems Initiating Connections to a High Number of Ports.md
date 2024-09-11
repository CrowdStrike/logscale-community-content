Could be indicative of a system with Falcon installed on it conducting network scanning.

```
#event_simpleName=/^(NetworkConnectIP4|ProcessRollup2)$/ 
| falconPID:=TargetProcessId | falconPID:=ContextProcessId
| UserID:=UserSid | UserID:=UID
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=NetworkConnectIP4}, {#event_simpleName=ProcessRollup2}])
| groupBy([aid, ComputerName, falconPID], function=([
	collect([FileName, CommandLine, UserName, UserID]), 
	count(RemotePort, as=uniquePortCount), 
	collect([RemotePort], separator=", ", limit=25), 
	count(RemoteAddressIP4, distinct=true, as=remoteIPcount)
	]), limit=max)
| FileName=* RemotePort=*
| test(uniquePortCount>25)
```