
```
correlate(
    // Search for grandparent process
    grandparent: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName!="explorer.exe" CommandLine=*
    } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
    // Search for parent process
    parent: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName="cmd.exe" CommandLine=*
          | aid <=>grandparent.aid
          | ParentProcessId<=>grandparent.TargetProcessId
          } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
    // Search for child process
    child: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName="powershell.exe" CommandLine=/\s-[e^]{1,2}[ncodema^]+\s/iF
          | aid<=>parent.aid
          | ParentProcessId<=>parent.TargetProcessId
          } include: [cid, aid, TargetProcessId, ParentProcessId, UserName,ComputerName, FileName, CommandLine],
sequence=true, within=10m)

//  Create ProcessTree
| ProcessLineage:=format(format="%s (%s)\n\t└ %s (%s)\n\t\t└ %s (%s)", field=[grandparent.FileName, grandparent.CommandLine, parent.FileName, parent.CommandLine, child.FileName, child.CommandLine])

// Make ComputerName value stick out
| Endpoint:=child.ComputerName

// Create Link to Process Explorer

| format("[Graph Explorer](/graphs/process-explorer/tree?id=pid:%s:%s&investigate=true&_cid=%s)", field=["child.aid", "child.TargetProcessId", "child.cid"], as="Graph Explorer")
```