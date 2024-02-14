```

(#event_simpleName=ProcessRollup2 ImageFileName=/\\psexec64\.exe/i ParentBaseFileName=/powershell\.exe/i)

| rename(field="ImageFileName", as="ChildImageFileName")
| rename(field="CommandLine", as="ChildCommandLine")
| join( { #event_simpleName=ProcessRollup2 ImageFileName=/powershell\.exe/i | ParentImageFileName := ImageFileName | ParentCmdLine := CommandLine | rename(field="ParentBaseFileName", as="GrandParentFileName")}, key=[aid, TargetProcessId], field=[aid, ParentProcessId], include=[GrandParentFileName, ParentImageFileName, ParentCmdLine] )
| select([aid, GrandParentFileName, ParentImageFileName, ParentCmdLine, ChildImageFileName, ChildCommandLine])

```