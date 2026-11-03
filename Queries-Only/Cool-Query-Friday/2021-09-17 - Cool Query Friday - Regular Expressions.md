---
title: "Regular Expressions"
date: 2021-09-17
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/ppzp59/20210917_cool_query_friday_regular_expressions/"
mitre: []
series: Cool Query Friday
---

# Regular Expressions

> Source: [https://www.reddit.com/r/crowdstrike/comments/ppzp59/20210917_cool_query_friday_regular_expressions/](https://www.reddit.com/r/crowdstrike/comments/ppzp59/20210917_cool_query_friday_regular_expressions/) — by Andrew-CS (CrowdStrike) — 2021-09-17

Welcome to our twenty-third installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
[...]
| rex field=fieldName "regex here"
[...]
```

## Query 2
```cql
event_platform=win event_simpleName=DnsRequest
| fields ComputerName, DomainName
| head 5
```

## Query 3
```cql
[...]
| rex field=DomainName ".*\.(?<DomainTLD>.*\..*)"
```

## Query 4
```cql
event_platform=win event_simpleName=DnsRequest
| fields ComputerName, DomainName
| rex field=DomainName ".*\.(?<DomainTLD>.*\..*)"
| table ComputerName DomainName DomainTLD
```

## Query 5
```cql
event_platform=win event_simpleName=ProcessRollup2 
| search FilePath="*\\Microsoft.Net\\*"
| head 5
```

## Query 6
```cql
[...]
| rex field=ImageFileName "\\\\Device\\\\HarddiskVolume\d+\\\\Windows\\\\Microsoft\.NET\\\\Framework(|64)\\\\v(?<dotNetVersion>\d+\.\d+\.\d+)\\\\.*"
[...]
```

## Query 7
```cql
event_platform=win event_simpleName=ProcessRollup2 
| search FilePath="*\\Microsoft.Net\\*"
| head 25
| rex field=ImageFileName "\\\\Device\\\\HarddiskVolume\d+\\\\Windows\\\\Microsoft\.NET\\\\Framework(|64)\\\\v(?<dotNetVersion>\d+\.\d+\.\d+)\\\\.*"
| stats values(FileName) as fileNames by ComputerName, dotNetVersion
```

## Query 8
```cql
event_platform=Lin event_simpleName=OsVersionInfo 
| rex field=OSVersionString "Linux\\s\\S+\\s(?<kernelVersion>\\S+)?\\s.*"
```

## Query 9
```cql
earliest=-24h event_platform=win event_simpleName=AgentOnline 
| rex field=AgentVersion "(?<baseAgentVersion>.*)\.\d+\.\d+"
```

## Query 10
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 
| rex field=CommandLine "(?<suspiciousCharacter>[^[:ascii:]]+)"
| where isnotnull(suspiciousCharacter)
| eval suspcisousCharacterCount=len(suspiciousCharacter)
| table FileName suspcisousCharacterCount suspiciousCharacter CommandLine
```

## Query 11
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3
| where isnotnull(CallStackModuleNames)
| head 50
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
| fields ComputerName FileName CallStackModuleNames loadedFile
```
