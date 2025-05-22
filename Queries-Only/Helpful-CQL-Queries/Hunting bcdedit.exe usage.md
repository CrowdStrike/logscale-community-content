```
#event_simpleName=ProcessRollup2 event_platform=Win FileName="bcdedit.exe"
| ProcessLineage:=format(format="%s\n\t└ %s", field=[ParentBaseFileName, FileName])
| regex("bcdedit(\.exe)?\"?\s+\/(?<operator>\w+)\s+(?<actions>.+$)", field=CommandLine, flags=iF, strict=false)
| groupBy([aid, ComputerName, UserName, ProcessLineage, operator, actions, CommandLine])
```