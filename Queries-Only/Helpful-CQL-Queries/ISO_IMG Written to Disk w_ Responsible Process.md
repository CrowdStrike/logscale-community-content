```
#event_simpleName=ProcessRollup2

| join({#event_simpleName=IsoExtensionFileWritten OR #event_simpleName=ImgExtensionFileWritten}, key=[aid, ContextProcessId], field=[aid, TargetProcessId], include=[TargetFileName])
| ImageFileName=/(\/|\\)(?<FileName>\w*\.?\w*)$/
| format(format="%s > %s > %s", field=[GrandParentBaseFileName, ParentBaseFileName, FileName], as="processLineage")
| match(file="fdr_aidmaster.csv", field=aid, include=ComputerName, ignoreCase=true, strict=false)
| table([aid, ComputerName, processLineage, CommandLine, TargetFileName])

```