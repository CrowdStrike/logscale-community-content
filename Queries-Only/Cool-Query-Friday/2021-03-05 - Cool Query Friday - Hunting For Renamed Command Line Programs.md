---
title: "Hunting For Renamed Command Line Programs"
date: 2021-03-05
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/lyhga8/20210305_cool_query_friday_hunting_for_renamed/"
mitre: []
series: Cool Query Friday
---

# Hunting For Renamed Command Line Programs

> Source: [https://www.reddit.com/r/crowdstrike/comments/lyhga8/20210305_cool_query_friday_hunting_for_renamed/](https://www.reddit.com/r/crowdstrike/comments/lyhga8/20210305_cool_query_friday_hunting_for_renamed/) — by Andrew-CS (CrowdStrike) — 2021-03-05

Okay, we're going to try something here. Welcome to the first "Cool Query Friday." We're going to (try!) to publish a new, cool threat hunting query every Friday to the community. The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
| inputlookup appinfo.csv
```

## Query 2
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 
| rename FileName as runningExe
```

## Query 3
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 
| rename FileName as runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| eval runningExe=lower(runningExe)
| eval FileName=lower(FileName)
```

## Query 4
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 
| rename FileName as runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| eval runningExe=lower(runningExe)
| eval FileName=lower(FileName)
| where runningExe!=FileName
```

## Query 5
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 
| rename FileName as runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| eval runningExe=lower(runningExe)
| eval FileName=lower(FileName)
| where runningExe!=FileName
| stats dc(aid) as "System Count" count(aid) as "Execution Count" values(runningExe) as "File On Disk" values(FileName) as "Cloud File Name" values(FileDescription) as "File Description" by SHA256HashData
```

## Query 6
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 
| rename FileName as runningExe
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName FileDescription
| eval runningExe=lower(runningExe)
| eval FileName=lower(FileName)
| where runningExe!=FileName
| search FileName=cmd.exe
| stats dc(aid) as "System Count" count(aid) as "Execution Count" values(runningExe) as "File On Disk" values(FileName) as "Cloud File Name" values(FileDescription) as "File Description" by SHA256HashData
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| search NOT FileName IN (cmd.exe, powershell.exe)
```
— [CS] Andrew-CS · comment score 1

```cql
| search NOT SHA256HashData IN (hash1, hash2)
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] yankeesfan01x:** Is there a way to exclude a specific file on disk by chance (say if you know it's a legit action)?

**A — [CS] Andrew-CS:** Sure thing. Add this between the first and the second line of the query... | search NOT FileName IN (cmd.exe, powershell.exe) You could also do by SHA256 | search NOT SHA256HashData IN (hash1, hash2)
