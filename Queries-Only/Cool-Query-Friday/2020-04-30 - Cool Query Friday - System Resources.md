---
title: "System Resources"
date: 2020-04-30
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/n1tbwn/20200430_cqf_system_resources/"
mitre: []
series: Cool Query Friday
---

# System Resources

> Source: [https://www.reddit.com/r/crowdstrike/comments/n1tbwn/20200430_cqf_system_resources/](https://www.reddit.com/r/crowdstrike/comments/n1tbwn/20200430_cqf_system_resources/) — by Andrew-CS (CrowdStrike) — 2020-04-30

Welcome to our ninth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_simpleName=SystemCapacity
| lookup aid_master aid OUTPUT ComputerName Version MachineDomain OU SiteName
```

## Query 2
```cql
| inputlookup aid_master
```

## Query 3
```cql
event_simpleName=SystemCapacity
| lookup aid_master aid OUTPUT ComputerName Version MachineDomain OU SiteName Timezone
```

## Query 4
```cql
event_simpleName=SystemCapacity
| lookup aid_master aid OUTPUT ComputerName Version MachineDomain OU SiteName Timezone
| eval CpuClockSpeed_decimal=round(CpuClockSpeed_decimal/1000,1)
| eval MemoryTotal_decimal=round(MemoryTotal_decimal/1.074e+9,2)
```

## Query 5
```cql
event_simpleName=SystemCapacity
| lookup aid_master aid OUTPUT ComputerName Version MachineDomain OU SiteName Timezone
| eval CpuClockSpeed_decimal=round(CpuClockSpeed_decimal/1000,1)
| eval MemoryTotal_decimal=round(MemoryTotal_decimal/1.074e+9,2)
| stats latest(CpuProcessorName) as "CPU" latest(CpuClockSpeed_decimal) as "CPU Clock Speed (GHz)" latest(PhysicalCoreCount_decimal) as "CPU Physical Cores" latest(LogicalCoreCount_decimal) as "CPU Logical Cores" latest(MemoryTotal_decimal) as "RAM (GB)" latest(aip) as "External IP" latest(LocalAddressIP4) as "Internal IP" by aid, ComputerName, MachineDomain, OU, SiteName, Version, Timezone
```

## Query 6
```cql
event_simpleName=SystemCapacity
| lookup aid_master aid OUTPUT ComputerName Version MachineDomain OU SiteName Timezone
| eval CpuClockSpeed_decimal=round(CpuClockSpeed_decimal/1000,1)
| eval MemoryTotal_decimal=round(MemoryTotal_decimal/1.074e+9,2)
| stats latest(CpuProcessorName) as "CPU" latest(CpuClockSpeed_decimal) as "CPU Clock Speed (GHz)" latest(PhysicalCoreCount_decimal) as "CPU Physical Cores" latest(LogicalCoreCount_decimal) as "CPU Logical Cores" latest(MemoryTotal_decimal) as "RAM (GB)" latest(aip) as "External IP" latest(LocalAddressIP4) as "Internal IP" by aid, ComputerName, MachineDomain, OU, SiteName, Version, Timezone
| rename aid as "Falcon AgentID" ComputerName as "Endpoint Name" Version as "Operating System" MachineDomain as "Domain" SiteName as "Site" Timezone as "System Clock Timezone"
```

## Query 7
```cql
[…]
| where MemoryTotal_deciaml<1
[…]
```

## Query 8
```cql
earliest=-7d event_simpleName=SystemCapacity
| eval CpuClockSpeed_decimal=round(CpuClockSpeed_decimal/1000,1)
| eval MemoryTotal_decimal=round(MemoryTotal_decimal/1.074e+9,2) 
| stats latest(MemoryTotal_decimal) as totalMemory latest(CpuClockSpeed_decimal) as cpuSpeed latest(LogicalCoreCount_decimal) as logicalCores by aid, cid
| stats sum(totalMemory) as totalMemory sum(cpuSpeed) as totalCPU sum(logicalCores) as totalCores dc(aid) as totalEndpoints
| eval avgMemory=round(totalMemory/totalEndpoints,2)
| eval avgCPU=round(totalCPU/totalEndpoints,2)
| eval avgCores=round(totalCores/totalEndpoints,2)
```
