https://www.reddit.com/r/crowdstrike/comments/qid1tj/20211029_cool_query_friday_cpu_ram_disk_firmware/

```
// Get 4 events of interest  
event_platform=Win  
| in(field="#event_simpleName", values=[AgentOnline,ResourceUtilization,SystemCapacity,ZeroTrustHostAssessment])  
  
// Use selfJoinFilter() to include only systems where all 4 events are in search window  
| selfJoinFilter(field=[aid], where=[{#event_simpleName=AgentOnline}, {#event_simpleName=ResourceUtilization}, {#event_simpleName=SystemCapacity}, {#event_simpleName=ZeroTrustHostAssessment}])  
  
// Aggregate by Agent ID  
| groupBy([aid], function=([selectLast([BiosManufacturer, ChasisManufacturer, CpuProcessorName, MemoryTotal,assessments.firmware_is_uefi, TpmFirmwareVersion, AvailableDiskSpace, AverageCpuUsage, AverageUsedRam])]), limit=max)  
  
// Format fields as required  
| unit:convert(AverageUsedRam, from="M", to="G")  
| UEFI:=upper("assessments.firmware_is_uefi") | drop(["assessments.firmware_is_uefi"])  
| unit:convert(MemoryTotal, to="G", binary=true)  
| default(value="-", field=[TpmFirmwareVersion,BiosManufacturer, ChasisManufacturer,CpuProcessorName, AverageCpuUsage, MemoryTotal, AverageUsedRam, AvailableDiskSpace], replaceEmpty=true)  
  
// Check to see if TPM Firmware version is reporting indicating TPM 2.0  
| case {  
TpmFirmwareVersion="-" | TPM:="-";  
* | TPM:="2.0";  
}  
| drop([TpmFirmwareVersion])  
  
// Merge data from AID Master  
| match(file="aid_master_main.csv", field=[aid], include=[Version, ComputerName])  
  
// Final aggregation to order fields  
| groupBy([aid, ComputerName, BiosManufacturer, ChasisManufacturer, Version, CpuProcessorName, AverageCpuUsage, MemoryTotal, AverageUsedRam, AvailableDiskSpace, UEFI, TPM], function=[], limit=max)
```