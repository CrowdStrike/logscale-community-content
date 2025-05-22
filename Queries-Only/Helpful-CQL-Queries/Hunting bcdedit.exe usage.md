```
// Get bcdedit.exe process executions
#event_simpleName=ProcessRollup2 event_platform=Win FileName="bcdedit.exe"

// Create process lineage tree for easier reading
| ProcessLineage:=format(format="%s\n\t└ %s\n\t\t└ %s", field=[GrandParentBaseFileName, ParentBaseFileName, FileName])

// Parse operator from bcdedit command if present
| regex("bcdedit(\.exe)?\"?\s+\/(?<operator>\w+)\s+(?<actions>.+$)", field=CommandLine, flags=iF, strict=false)

// Aggregate by command line arguments
| groupBy(CommandLine, function=([count(), collect([ProcessLineage, operator, actions])]))
```