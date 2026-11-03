---
title: "The Cheat Sheet"
date: 2021-09-10
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/plkwqu/20210910_cool_query_friday_the_cheat_sheet/"
mitre: []
series: Cool Query Friday
---

# The Cheat Sheet

> Source: [https://www.reddit.com/r/crowdstrike/comments/plkwqu/20210910_cool_query_friday_the_cheat_sheet/](https://www.reddit.com/r/crowdstrike/comments/plkwqu/20210910_cool_query_friday_the_cheat_sheet/) — by Andrew-CS (CrowdStrike) — 2021-09-10

Welcome to our twenty-second installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
[...]
| convert ctime(ProcessStartTime_decimal)
[...]
```

## Query 2
```cql
earliest=-1m event_simpleName IN (ProcessRollup2, DnsRequest)
| convert ctime(ProcessStartTime_decimal) ctime(ContextTimeStamp_decimal)
| table event_simpleName ProcessStartTime_decimal ContextTimeStamp_decimal
```

## Query 3
```cql
earliest=-1m event_simpleName IN (ProcessRollup2, DnsRequest)
| convert ctime(ProcessStartTime_decimal) ctime(ContextTimeStamp_decimal)
| table event_simpleName _time ProcessStartTime_decimal ContextTimeStamp_decimal
```

## Query 4
```cql
[...]
| convert ctime(timestamp)
[...]
```

## Query 5
```cql
[...]
| eval timestamp=timestamp/1000
| convert ctime(timestamp)
[...]
```

## Query 6
```cql
earliest=-5m event_simpleName IN (ProcessRollup2, EndofProcess) 
| stats values(ProcessStartTime_decimal) as startTime, values(ProcessEndTime_decimal) as endTime by aid, TargetProcessId_decimal, FileName
| eval runTimeSeconds=endTime-startTime
| where isnotnull(endTime)
| convert ctime(startTime) ctime(endTime)
```

## Query 7
```cql
[...]
| eval myUTCoffset=-4
| eval myLocalTime=ProcessStartTime_decimal+(60*60*myUTCoffset)
[...]
```

## Query 8
```cql
earliest=-1m event_simpleName IN (ProcessRollup2)
| eval myUTCoffset=-7
| eval myLocalTime=ProcessStartTime_decimal+(myUTCoffset*60*60)
| table FileName _time ProcessStartTime_decimal myLocalTime
| rename ProcessStartTime_decimal as endpointSystemClockUTC, _time as cloudTimeUTC
| convert ctime(cloudTimeUTC), ctime(endpointSystemClockUTC), ctime(myLocalTime)
```

## Query 9
```cql
[...]
| eval endpointTime=mvappend(ProcessStartTime_decimal, ContextTimeStamp_decimal)
[...]
```

## Query 10
```cql
earliest=-1m event_simpleName IN (ProcessRollup2, DnsRequest)
| eval endpointTime=mvappend(ContextTimeStamp_decimal, ProcessStartTime_decimal)
| table event_simpleName _time endpointTime
| convert ctime(endpointTime)
```

## Query 11
```cql
[...]
| eval falconPID=mvappend(TargetProcessId_decimal, ContextProcessId_decimal)
[...]
```

## Query 12
```cql
earliest=-60m event_platform=win event_simpleName IN (OsVersionInfo)
| eval systemType=case(ProductType_decimal=1, "Workstation", ProductType_decimal=2, "Domain Controller", ProductType_decimal=3, "Server")
| table ComputerName ProductName systemType
```

## Query 13
```cql
[...]
| eval shortCmd=substr(CommandLine,1,250)
[...]
```

## Query 14
```cql
earliest=-5m event_simpleName IN (ProcessRollup2)
| eval shortCmd=substr(CommandLine,1,250)
| eval FullCmdCharCount=len(CommandLine)
| where FullCmdCharCount>250
| table ComputerName FileName FullCmdCharCount shortCmd CommandLine
```

## Query 15
```cql
earliest=-15m event_simpleName=DnsRequest
| rex field=DomainName "[@\.](?<tlDomain>\w+\.\w+)$"
| stats dc(DomainName) as subDomainCount, values(DomainName) as subDomain by tlDomain
| sort - subDomainCount
```

## Query 16
```cql
CHEAT SHEET

*** epoch to human readable ***

| convert ctime(ProcessStartTime_decimal)

*** combine Context and Target timestamps **

| eval endpointTime=mvappend(ProcessStartTime_decimal, ContextTimeStamp_decimal)

*** UTC Localization ***

| eval myUTCoffset=-4
| eval myLocalTime=ProcessStartTime_decimal+(60*60*myUTCoffset)

*** combine Falcon Process UUIDs ***

| eval falconPID=mvappend(TargetProcessId_decimal, ContextProcessId_decimal)

*** string swaps ***

| eval systemType=case(ProductType_decimal=1, "Workstation", ProductType_decimal=2, "Domain Controller", ProductType_decimal=3, "Server")

*** shorten string ***

| eval shortCmd=substr(CommandLine,1,250)

*** regex field ***

rex field=DomainName "[@\.](?<tlDomain>\w+\.\w+)$"
```
