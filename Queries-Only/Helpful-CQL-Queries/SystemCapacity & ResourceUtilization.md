```
#event_simpleName=/^(SystemCapacity|ResourceUtilization)$/

| groupBy(aid, function=([selectLast([CpuProcessorName, PhysicalCoreCount, LogicalCoreCount, AverageCpuUsage, MemoryTotal, MaxUsedRam, AverageUsedRam, MaxUsedRam, AvailableDiskSpace])]))
| CpuProcessorName=* AND AvailableDiskSpace=*
| percent := "%"
| gb := "GB"
| MemoryTotal := (MemoryTotal/1074000000)
| MemoryTotal := format("%,.2f", field=MemoryTotal)
| MaxUsedRam := (MaxUsedRam/1024)
| MaxUsedRam := format("%,.2f", field=MaxUsedRam)
| AverageUsedRam := (AverageUsedRam/1024)
| AverageUsedRam := format("%,.2f", field=AverageUsedRam)
| AveragePercentUsedRam := (AverageUsedRam/MemoryTotal)*100
| AveragePercentUsedRam := format("%,.2f", field=AveragePercentUsedRam)
| concat([AveragePercentUsedRam, percent], as="AveragePercentUsedRam")
| concat([MaxUsedRam, gb], as="MaxUsedRam")
| concat([MemoryTotal, gb], as="MemoryTotal")
| concat([AverageUsedRam, gb], as="AverageUsedRam")
| concat([AverageCpuUsage, percent], as="AverageCpuUsage")
| concat([AvailableDiskSpace, gb], as="AvailableDiskSpace")
| drop([gb, percent])
| match(file="fdr_aidmaster.csv", field=aid, include=ComputerName, ignoreCase=true, strict=false)
| select([aid, ComputerName, CpuProcessorName, PhysicalCoreCount, LogicalCoreCount, AverageCpuUsage, MemoryTotal, MaxUsedRam, AverageUsedRam, AveragePercentUsedRam, MaxUsedRam, AvailableDiskSpace])

```