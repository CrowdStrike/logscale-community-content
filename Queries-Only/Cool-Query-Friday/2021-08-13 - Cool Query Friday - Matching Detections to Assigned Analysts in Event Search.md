---
title: "Matching Detections to Assigned Analysts in Event Search"
date: 2021-08-13
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/p3mt5g/20210813_cool_query_friday_matching_detections_to/"
mitre: []
series: Cool Query Friday
---

# Matching Detections to Assigned Analysts in Event Search

> Source: [https://www.reddit.com/r/crowdstrike/comments/p3mt5g/20210813_cool_query_friday_matching_detections_to/](https://www.reddit.com/r/crowdstrike/comments/p3mt5g/20210813_cool_query_friday_matching_detections_to/) — by Andrew-CS (CrowdStrike) — 2021-08-13

Welcome to our twenty-first installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
index=json  EventType=Event_ExternalApiEvent 
| stats values(ExternalApiType)
```

## Query 2
```cql
index=json EventType=Event_ExternalApiEvent ExternalApiType=Event_UserActivityAuditEvent 
| stats values(OperationName) as OperationName
```

## Query 3
```cql
index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent
| rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value
```

## Query 4
```cql
[...]
| eval data = mvzip(key,value)
```

## Query 5
```cql
index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent
| rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value
| eval data = mvzip(key,value)
| table ExternalApiType data
| where isnotnull(data)
```

## Query 6
```cql
index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent
| rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value
| eval data = mvzip(key,value)
| rex field=data "detection_id,ldt:(?<aid>.*?):(?<detectId>-?\\d+)?"
| rex field=data "assigned_to,(?<assigned_to>.*)"
| rex field=data "assigned_to_uid,(?<assigned_to_uid>.*)"
```

## Query 7
```cql
| rex field=data "detection_id,ldt:(?<aid>.*?):(?<detectId>-?\\d+)?"
```

## Query 8
```cql
index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent
| rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value
| eval data = mvzip(key,value)
| rex field=data "detection_id,.*:(?<aid>.*?):(?<detectId>-?\\d+)?"
| rex field=data "assigned_to,(?<assigned_to>.*)"
| rex field=data "assigned_to_uid,(?<assigned_to_uid>.*)" 
| eval detectId="ldt:".aid.":".detectId
| table ExternalApiType, UTCTimestamp, aid, AgentIdString, ComputerName, FileName, FilePath, CommandLine, DetectId, detectId, assigned_to, assigned_to_uid, DetectName, Tactic, Technique, SeverityName, FalconHostLink
```

## Query 9
```cql
[...]
| eval detectId=mvappend(DetectId, detectId)
| eval aid=mvappend(aid, AgentIdString)
```

## Query 10
```cql
[...]
| stats count(SeverityName) as totalBehaviors, values(ComputerName) as computerName, last(UTCTimestamp) as timeStamp, values(assigned_to) as assignedTo, last(assigned_to) as assignedToLast, values(DetectName) as detectName, values(Tactic) as tactic, values(Technique) as technique, values(SeverityName) as severityNames, values(FileName) as fileName, values(FilePath) as filePath, values(CommandLine) as commandLine, values(FalconHostLink) as falconLink by detectId
```

## Query 11
```cql
[...]
| where isnotnull(assignedTo)
| where isnotnull(detectName)
| eval timeStamp=timeStamp/1000
| convert ctime(timeStamp)
| sort + timeStamp
```

## Query 12
```cql
index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent
| rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value
| eval data = mvzip(key,value)
| rex field=data "detection_id,.*:(?<aid>.*?):(?<detectId>-?\\d+)?"
| rex field=data "assigned_to,(?<assigned_to>.*)"
| rex field=data "assigned_to_uid,(?<assigned_to_uid>.*)" 
| eval detectId="ldt:".aid.":".detectId
| table ExternalApiType, UTCTimestamp, aid, AgentIdString, ComputerName, FileName, FilePath, CommandLine, DetectId, detectId, assigned_to, assigned_to_uid, DetectName, Tactic, Technique, SeverityName, FalconHostLink
| eval detectId=mvappend(DetectId, detectId)
| eval aid=mvappend(aid, AgentIdString)
| stats count(SeverityName) as totalBehaviors, values(ComputerName) as computerName, last(UTCTimestamp) as timeStamp, values(assigned_to) as assignedTo, last(assigned_to) as assignedToLast, values(DetectName) as detectName, values(Tactic) as tactic, values(Technique) as technique, values(SeverityName) as severityNames, values(FileName) as fileName, values(FilePath) as filePath, values(CommandLine) as commandLine, values(FalconHostLink) as falconLink by detectId
| where isnotnull(assignedTo)
| where isnotnull(detectName)
| eval timeStamp=timeStamp/1000
| convert ctime(timeStamp)
| sort + timeStamp
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
earliest=-24h index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent
| eval OperationName=lower(OperationName)
| rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value
| eval data = mvzip(key,value)
| rex field=data "detection_id,.*:(?<aid>.*?):(?<detectId>-?\\d+)?"
| eval detectId="ldt:".aid.":".detectId
| rex field=data "assigned_to,(?<assigned_to>.*)"
| rex field=data "assigned_to_uid,(?<assigned_to_uid>.*)"
| rex field=data "new_state,(?<detectionState>.*)"
| table *
| eval detectId=mvappend(DetectId, detectId)
| eval aid=mvappend(aid, AgentIdString)
| lookup local=true aid_master aid OUTPUT FalconGroupingTags
| eval FalconGroupingTags=split(FalconGroupingTags,";")
| stats values(ComputerName) as computerName, values(FalconGroupingTags) as FalconTags,
last(UTCTimestamp) as timeStamp, values(FileName) as fileNames, values(SHA256String) as sha256Values, values(assigned_to) as assignedTo, last(detectionState) as detectionState, values(DetectName) as detectName, max(Severity) as Severity, values(Tactic) as tactic, values(Technique) as technique, values(SeverityName) as SeverityNames values(FalconHostLink) as falconLink by aid, detectId
| where isnotnull(falconLink)
| eval Severity=case(Severity=1, "Informational", Severity=2, "Low", Severity=3, "Medium", Severity=4, "High", Severity=5, "Critical")
| eval timeStamp=timeStamp/1000
| convert ctime(timeStamp)
| sort + timeStamp
| fillnull assignedTo value="-"
| fillnull detectionState value="new"
```
— [CS] Andrew-CS · comment score 3

### Q&A

**Q — [Community] BingBongTheArcher23:** Is there a way to include the corresponding filehash information or the status (TP/FP/Ignored/etc) of the events?

**A — [CS] Andrew-CS:** Yup! earliest=-24h index=json AND (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update) OR ExternalApiType=Event_DetectionSummaryEvent | eval OperationName=lower(OperationName) | rename AuditKeyValues{}.Key AS key AuditKeyValues{}.ValueString AS value | eval data = mvzip(key,value) | rex field=data "detection_id,.*:(?<aid>.*?):(?<detectId>-?\\d+)?" | eval detectId="ldt:".aid.":".detectId | rex field=data "assigned_to,(?<assigned_to>.*)" | rex field=data "assigned_to_u …
