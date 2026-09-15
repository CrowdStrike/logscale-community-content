---
title: "Parsing the Call Stack"
date: 2021-04-23
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/mwuz92/20210423_cool_query_friday_parsing_the_call_stack/"
mitre: []
series: Cool Query Friday
---

# Parsing the Call Stack

> Source: [https://www.reddit.com/r/crowdstrike/comments/mwuz92/20210423_cool_query_friday_parsing_the_call_stack/](https://www.reddit.com/r/crowdstrike/comments/mwuz92/20210423_cool_query_friday_parsing_the_call_stack/) — by Andrew-CS (CrowdStrike) — 2021-04-23

Welcome to our eighth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=win event_simpleName=ProcessRollup2
| where isnotnull(CallStackModuleNames) 
| table ComputerName FileName CommandLine CallStackModuleNames
```

## Query 2
```cql
0<-1>\Device\HarddiskVolume1\Windows\System32\ntdll.dll+0x9f8a4:0x1ec000:0x6e7b7e33|\Device\HarddiskVolume1\Windows\System32\KernelBase.dll+0x5701e:0x294000:0xc97af40a|1+0x56d84|1+0x55a0d|1+0x54dda|1+0x547ed|0+0x25d37|0+0x285e9|0+0x28854|0+0x2887e|0+0x29551|0+0x26921|0+0x23238|0+0x22794|0+0xd53e9|0+0x7837b|0+0x78203|0+0x781ae
```

## Query 3
```cql
event_platform=win event_simpleName=ProcessRollup2 CallStackModuleNames=*JIT-DOTNET*
| table ComputerName FileName CommandLine CallStackModuleNames
```

## Query 4
```cql
event_platform=win event_simpleName=ProcessRollup2 CallStackModuleNames=*
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
```

## Query 5
```cql
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
```

## Query 6
```cql
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
```

## Query 7
```cql
event_platform=win event_simpleName=ProcessRollup2 CallStackModuleNames=*
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
| table ComputerName FileName CallStackModuleNames loadedFile
| head 2
```

## Query 8
```cql
event_platform=win event_simpleName=ProcessRollup2 CallStackModuleNames=*
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
| stats dc(SHA256HashData) as SHA256values values(loadedFile) as loadedFiles dc(aid) as endpointCount count(aid) as loadCount by FileName
| eval loadedFiles=mvfilter(match(loadedFiles, "\\\\temp\\\\"))
| where isnotnull(loadedFiles)
| sort + loadCount
```

## Query 9
```cql
| stats dc(SHA256HashData) as SHA256values values(loadedFile) as loadedFiles dc(aid) as endpointCount count(aid) as loadCount by FileName
```

## Query 10
```cql
| eval loadedFiles=mvfilter(match(loadedFiles, "\\\\temp\\\\"))
```

## Query 11
```cql
| where isnotnull(loadedFiles)
```

## Query 12
```cql
| sort + loadCount
```

## Query 13
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 CallStackModuleNames=*
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
| stats dc(SHA256HashData) as SHA256values values(loadedFile) as loadedFiles dc(aid) as endpointCount count(aid) as loadCount by FileName
| eval loadedFiles=mvfilter(match(loadedFiles, "\\\\temp\\\\"))
| where isnotnull(loadedFiles)
| sort + loadCount
```

## Query 14
```cql
event_platform=win event_simpleName=ProcessRollup2 CallStackModuleNames=*
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n ".*\\\\Device\\\\HarddiskVolume\d+(?<loadedFile>.*(\.dll|\.exe)).*"
| stats dc(SHA256HashData) as SHA256count values(loadedFile) as loadedFiles dc(aid) as endpointCount count(aid) as loadCount by FileName
| eval loadedFiles=mvfilter(!match(loadedFiles, "\\\\Windows\\\\System32\\\\*"))
| eval loadedFiles=mvfilter(!match(loadedFiles, "\\\\Windows\\\\SysWOW64\\\\*"))
| eval loadedFiles=mvfilter(!match(loadedFiles, "\\\\Windows\\\\assembly\\\\*"))
| where isnotnull(loadedFiles)
| sort + loadCount
```

## Query 15
```cql
event_platform=win event_simpleName=ProcessRollup2 
| rename TargetProcessId_decimal AS ContextProcessId_decimal, CallStackModuleNames as exeCallStack
| join aid, ContextProcessId_decimal
    [search event_platform=win event_simpleName=CreateThreadReflectiveDll]
| eval ShortCmd=substr(CommandLine,1,100)
| eval CallStackModuleNames=split(CallStackModuleNames, "|")
| eval n=mvfilter(match(CallStackModuleNames, ".*exe") OR match(CallStackModuleNames, ".*dll"))
| rex field=n "(?<callStack>.*(\.dll|\.exe)).*"
| table ContextTimeStamp_decimal ComputerName UserName FileName ShortCmd ReflectiveDllName callStack
| convert ctime(ContextTimeStamp_decimal)
| rename ContextTimeStamp_decimal as dllReflectiveLoadTime
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
[...]
| eval n=mvfilter(match(CallStackModuleNames, ".*\.exe.*") OR match(CallStackModuleNames, ".*\.dll.*"))
[...]
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] SnooCookies3976:** How does CreateThreadReflectiveDll compare to ReflectiveDllOpenProcess?

**A — [CS] Andrew-CS:** >CreateThreadReflectiveDll Signals there was a reflectively loaded DLL on the callstack, or that the target address is in a reflectively loaded DLL. >ReflectiveDllOpenProcess Signals a userspace thread attempted to open a process which appeared to originate from a reflectively loaded DLL.

**Q — [Community] AnalogJones:** "Cool Query Friday" is awesome. I am new to this column and I've been playing with all of the queries offered! I was having trouble with this Call Stack thread, though. Starting on Step #3 I would continue to get Event data, but no stats/visualization data. Can you help me understand what is broken? …

**A — [CS] Andrew-CS:** >event\_platform=win event\_simpleName=ProcessRollup2 CallStackModuleNames=\* > >| eval CallStackModuleNames=split(CallStackModuleNames, "|") > >| eval n=mvfilter(match(CallStackModuleNames, "exe") OR match(CallStackModuleNames, "dll")) > >| rex field=n ".\*\\\\\\\\Device\\\\\\\\HarddiskVolume\\d+(?<loadedFile>.\*(\\.dll|\\.exe)).\*" > >| table ComputerName FileName CallStackModuleNames loadedFile > >| head 2 Hi there. Both should work as what is in those quotes (in the bolded line) is a regular …
