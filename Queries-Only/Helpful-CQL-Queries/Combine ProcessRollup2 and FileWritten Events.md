```
(#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/(winword|excel)\.exe/i) OR (#event_simpleName=ZipFileWritten event_platform=Win)
| falconPID:=ContextProcessId | falconPID:=TargetProcessId
| selfJoinFilter(field=[aid, falconPID], where=[{#event_simpleName=ProcessRollup2}, {#event_simpleName=ZipFileWritten}], prefilter=true)
| case{
    ImageFileName=*  | ImageFileName=/(\\Device\\HarddiskVolume\d+|\/)?(?<ExecutingFilePath>(\\|\/).+(\\|\/))(?<ExecutingFileName>.+)$/i;
    TargetFileName=* | TargetFileName=/(\\Device\\HarddiskVolume\d+|\/)?(?<WrittenFilePath>(\\|\/).+(\\|\/))(?<WrittenFileName>.+)$/i;
}
| groupBy([aid, falconPID], function=([count(#event_simpleName, distinct=true, as=eventCount), collect([ExecutingFileName, WrittenFileName])]))
| eventCount > 1
| drop([eventCount])
```