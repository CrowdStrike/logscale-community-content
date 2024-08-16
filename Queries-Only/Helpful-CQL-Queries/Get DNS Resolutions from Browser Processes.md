```
// Get all process execution and DNS events on Windows
(#event_simpleName=ProcessRollup2 OR #event_simpleName=DnsRequest) event_platform=Win
| ComputerName=~wildcard(?ComputerName, ignoreCase=true)
// Normalize file name value across both events
| fileName:=concat([FileName, ContextBaseFileName])
// Make sure responsible process is a web browser
| in(field="fileName", values=[chrome.exe, firefox.exe, msedge.exe], ignoreCase=true)
// Normalize Falcon UPID
| falconPID:=TargetProcessId | falconPID:=ContextProcessId
// Use selfJoinFilter to make sure execution and DNS resolution occured under the same UPID value
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=ProcessRollup2}, {#event_simpleName=DnsRequest}])
// Aggregate results
| groupBy([aid, falconPID], function=([collect([ComputerName, UserName, fileName, DomainName])]))
```
