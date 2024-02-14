```
(#event_simpleName=ProcessRollup2 ImageFileName=/\\powershell(_ise)?\.exe/i) OR (#event_simpleName=EndOfProcess event_platform=Win CLICreationCount>0)
| selfJoinFilter([aid, TargetProcessId], where=[{#event_simpleName=ProcessRollup2}, {#event_simpleName=EndOfProcess}], prefilter=true)
| regex(".+\\\(?<FileName>.+$)", field=ImageFileName, strict=false)
| groupBy([aid, TargetProcessId], function=([count(#event_simpleName, distinct=true, as=eventCount), min(ProcessStartTime, as=processStartTime), max(ContextTimeStamp, as=processEndTime), collect([CLICreationCount, FileName])]))
| test(eventCount==2)
| processStartTime := processStartTime*1000
| processEndTime := processEndTime*1000
| runTime := processEndTime-processStartTime
| formatDuration(runTime, from=ms, precision=4, as=programRunTime)
| formatTime(format="%F %T.%L", field=processStartTime, as="processStartTime")
| formatTime(format="%F %T.%L", field=processEndTime, as="processEndTime")
| drop([eventCount, runTime])

```

[[selfJoinFilter]] | [[regex]] | [[regex - extraction]] | [[groupBy]] | [[test]] | [[formatDuration]] | [[formatTime]] | [[drop]] 