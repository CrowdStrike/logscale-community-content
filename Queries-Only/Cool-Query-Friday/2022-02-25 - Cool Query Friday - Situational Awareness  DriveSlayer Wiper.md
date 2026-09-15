---
title: "Situational Awareness \\\\ DriveSlayer Wiper"
date: 2022-02-25
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/t0vhe6/20220225_cool_query_friday_situational_awareness/"
mitre: []
series: Cool Query Friday
---

# Situational Awareness \\ DriveSlayer Wiper

> Source: [https://www.reddit.com/r/crowdstrike/comments/t0vhe6/20220225_cool_query_friday_situational_awareness/](https://www.reddit.com/r/crowdstrike/comments/t0vhe6/20220225_cool_query_friday_situational_awareness/) — by Andrew-CS (CrowdStrike) — 2022-02-25

Welcome to our thirty-eighth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
event_platform=win event_simpleName IN (PeFileWritten) AND FileName="*.sys" AND FilePath="*\\Windows\\System32\\drivers\\"
| rex field=FileName "(?<fileNameNoExtension>.*)\..*"
| eval fileNameLength=len(fileNameNoExtension)
| search fileNameLength=4 
| eval endpointTime=coalesce(ContextTimeStamp_decimal, ProcessStartTime_decimal)
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
| table endpointTime, aid, ComputerName, event_simpleName, falconPID, FileName, FilePath, fileNameNoExtension, fileNameLength, SHA256HashData
| sort + endpointTime
| convert ctime(endpointTime)
```

## Query 2
```cql
event_platform=win event_simpleName IN (Asep*) 
| search RegStringValue="*\\Windows\\system32\\Drivers\\*.sys"
| rex field=RegObjectName ".*\\\(?<regObjNameNoExtension>.*)" 
| eval regObjNameNoExtensionLength=len(regObjNameNoExtension)
| search regObjNameNoExtensionLength=4
| table ContextTimeStamp_decimal, aid, ComputerName, UserName, RegObjectName, regObjNameNoExtension, regObjNameNoExtensionLength, RegStringValue
| convert ctime(ContextTimeStamp_decimal)
| rename ContextTimeStamp_decimal as registryModifiedTime
```

## Query 3
```cql
event_platform=win event_simpleName=DriverLoad CertificateThumbprint=696b5cb5d85721807d3942c73b317a062e22cf2a 
| rex field=FileName "(?<baseFileName>.*)\.sys" 
| eval baseFileLength=len(baseFileName) 
| search baseFileLength=4 
| table _time, aid, ComputerName, FileName, baseFileName, baseFileLength, FilePath, SHA256HashData, CertificateThumbprint
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] jarks_20:** Andrew...is there any goodies :) that you can share in regards with whispergate?

**A — [CS] Andrew-CS:** Hi there, for Falcon Intelligence customers there is a very detailed report here: CSA-220189. We track this activity cluster to the threat actor [EMBER BEAR](https://falcon.crowdstrike.com/intelligence-v2/actors/ember-bear/summary).
