Uses `correlate()` to hunt a three-level Windows process lineage: any process (grandparent), spawning `cmd.exe` (parent), spawning an encoded `powershell.exe` command (child). The `sequence=true` parameter requires the events to occur in that order within 10 minutes.

The grandparent search matches nearly every process event. In large environments, narrow it (for example by `FileName` or `CommandLine`) to keep `correlate()` within its result limits.

```
correlate(
    // Search for grandparent process
    grandparent: {
        #repo="base_sensor" #event_simpleName=ProcessRollup2 event_platform=Win FileName!="explorer.exe" CommandLine=*
    } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
    // Search for parent process
    parent: {
        #repo="base_sensor" #event_simpleName=ProcessRollup2 event_platform=Win FileName="cmd.exe" CommandLine=*
          | aid <=> grandparent.aid
          | ParentProcessId <=> grandparent.TargetProcessId
          } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
    // Search for child process
    child: {
        #repo="base_sensor" #event_simpleName=ProcessRollup2 event_platform=Win FileName="powershell.exe" CommandLine=/\s-[e^]{1,2}[ncodema^]+\s/iF
          | aid <=> parent.aid
          | ParentProcessId <=> parent.TargetProcessId
          } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
sequence=true, within=10m)

// Create process tree
| ProcessLineage:=format(format="%s (%s)\n\t└ %s (%s)\n\t\t└ %s (%s)", field=[grandparent.FileName, grandparent.CommandLine, parent.FileName, parent.CommandLine, child.FileName, child.CommandLine])

// Make ComputerName value stick out
| Endpoint:=child.ComputerName

// Create link to Process Explorer
| format("[Graph Explorer](/graphs/process-explorer/tree?id=pid:%s:%s&investigate=true&_cid=%s)", field=["child.aid", "child.TargetProcessId", "child.cid"], as="Graph Explorer")
```
