```
(#event_simpleName=/^(SystemCapacity|ResourceUtilization)$/) OR (#repo=sensor_metadata #data_source_name=aidmaster)
| case {
    event_platform=Lin | ProductType:=3;
    event_platform=Mac | ProductType:=1;
    *;
}
| $falcon/helper:enrich(field=ProductType)
| selfJoinFilter(field=[aid], where=[{#event_simpleName=SystemCapacity},{#event_simpleName=ResourceUtilization}, {#repo=sensor_metadata #data_source_name=aidmaster}])
| groupBy([aid], function=([selectLast([ComputerName, event_platform, ProductType, AgentVersion, Version, MachineDomain, OU, SiteName, CpuProcessorName, PhysicalCoreCount, LogicalCoreCount, AverageCpuUsage, MaxCpuUsage, MemoryTotal, AverageUsedRam, MaxUsedRam, UsedDiskSpace, AvailableDiskSpace])]))
| PercentDiskUsed:=AvailableDiskSpace/(UsedDiskSpace+AvailableDiskSpace) | PercentDiskUsed:=format(format="%,.2f %%", field=[PercentDiskUsed])
| MemoryTotal:=(MemoryTotal/1024/1024/1024) | MemoryTotal:=round(MemoryTotal) | MemoryTotal:=format(format="%s GB", field=[MemoryTotal])
| AverageUsedRam:=(AverageUsedRam/1024) | AverageUsedRam:=format(format="%,.2f GB", field=[AverageUsedRam])
| MaxUsedRam:=(MaxUsedRam/1024) | MaxUsedRam:=format(format="%,.2f GB", field=[MaxUsedRam])
| AverageCpuUsage:= format(format="%s %%", field=[AverageCpuUsage])
| MaxCpuUsage:= format(format="%s %%", field=[MaxCpuUsage])
| default(value="-", field=[ComputerName, event_platform, ProductType, AgentVersion, Version, MachineDomain, OU, SiteName, CpuProcessorName, PhysicalCoreCount, LogicalCoreCount, AverageCpuUsage, MaxCpuUsage, MemoryTotal, AverageUsedRam, MaxUsedRam, UsedDiskSpace, AvailableDiskSpace, PercentDiskUsed], replaceEmpty=true)
| rename(field="aid", as="Agent ID")
| rename(field="ComputerName", as="Endpoint")
| rename(field="event_platform", as="Platform")
| rename(field="ProductType", as="Type")
| rename(field="AgentVersion", as="Falcon Version")
| rename(field="Version", as="OS")
| rename(field="MachineDomain", as="Domain")
| rename(field="SiteName", as="Site")
| rename(field="CpuProcessorName", as="CPU")
| rename(field="PhysicalCoreCount", as="Physical Cores")
| rename(field="LogicalCoreCount", as="Logical Cores")
| rename(field="AverageCpuUsage", as="Avg. CPU")
| rename(field="MaxCpuUsage", as="Max. CPU")
| rename(field="AverageUsedRam", as="Avg. RAM")
| rename(field="MaxUsedRam", as="Max. RAM")
| rename(field="PercentDiskUsed", as="% Disk Used")
| table(["Agent ID", "Endpoint", "Platform", "Type", "Falcon Version", "OS", "Domain", "Site", "CPU", "Physical Cores", "Logical Cores", "Avg. CPU", "Max. CPU", "Avg. RAM", "MaxUsedRam", "% Disk Used"], limit=20000)
```