---
title: "Time To Assign, Time To Resolve, and Time To Close"
date: 2022-02-11
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/spx5zu/20220211_cool_query_friday_time_to_assign_time_to/"
mitre: []
series: Cool Query Friday
---

# Time To Assign, Time To Resolve, and Time To Close

> Source: [https://www.reddit.com/r/crowdstrike/comments/spx5zu/20220211_cool_query_friday_time_to_assign_time_to/](https://www.reddit.com/r/crowdstrike/comments/spx5zu/20220211_cool_query_friday_time_to_assign_time_to/) — by Andrew-CS (CrowdStrike) — 2022-02-11

Welcome to our thirty-sixth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
index=json ExternalApiType IN (*)
| stats values(ExternalApiType)
```

## Query 2
```cql
[...]
| eval detection_id=coalesce(DetectId, mvfilter(match('AuditKeyValues{}.ValueString', "ldt.*")))
| eval response_time=if('AuditKeyValues{}.ValueString' IN ("true_positive", "false_positive"), _time, null())
| eval assign_time=if('AuditKeyValues{}.Key'="assigned_to", _time, null())
```

## Query 3
```cql
[...]
| stats values(ComputerName) as ComputerName, max(Severity) as Severity, values(Tactic) as Tactics, values(Technique) as Techniques, earliest(_time) as FirstDetect earliest(assign_time) as FirstAssign, earliest(response_time) as ResolvedTime by detection_id
```

## Query 4
```cql
[...]
| eval MinutesToAssign=round((FirstAssign-FirstDetect)/60,0)
| eval HoursFromAssignToClose=round((ResolvedTime-FirstAssign)/60/60,2)
| eval DaysFromDetectToClose=round((ResolvedTime-FirstDetect)/60/60/24,2)
```

## Query 5
```cql
| where isnotnull(ComputerName)
| eval Severity=case(Severity=1, "Informational", Severity=2, "Low", Severity=3, "Medium", Severity=4, "High", Severity=5, "Critical")
| convert ctime(FirstDetect) ctime(FirstAssign) ctime(ResolvedTime)
| fillnull value="-" FirstAssign, ResolvedTime, MinutesToAssign, HoursFromAssignToClose, DaysFromDetectToClose 
| table ComputerName, Severity, Tactics, Techniques, FirstDetect, FirstAssign, MinutesToAssign, ResolvedTime, HoursFromAssignToClose, DaysFromDetectToClose, detection_id 
| sort + FirstDetect
```

## Query 6
```cql
index=json ExternalApiType=Event_DetectionSummaryEvent OR (ExternalApiType=Event_UserActivityAuditEvent AND OperationName=detection_update (AuditKeyValues{}.ValueString IN ("true_positive", "false_positive","new_detection") OR AuditKeyValues{}.Key="assigned_to"))
| eval detection_id=coalesce(DetectId, mvfilter(match('AuditKeyValues{}.ValueString', "ldt.*")))
| eval response_time=if('AuditKeyValues{}.ValueString' IN ("true_positive", "false_positive"), _time, null())
| eval assign_time=if('AuditKeyValues{}.Key'="assigned_to", _time, null())
| stats values(ComputerName) as ComputerName, max(Severity) as Severity, values(Tactic) as Tactics, values(Technique) as Techniques, earliest(_time) as FirstDetect earliest(assign_time) as FirstAssign, earliest(response_time) as ResolvedTime by detection_id
| eval MinutesToAssign=round((FirstAssign-FirstDetect)/60,0)
| eval HoursFromAssignToClose=round((ResolvedTime-FirstAssign)/60/60,2)
| eval DaysFromDetectToClose=round((ResolvedTime-FirstDetect)/60/60/24,2)
| where isnotnull(ComputerName)
| eval Severity=case(Severity=1, "Informational", Severity=2, "Low", Severity=3, "Medium", Severity=4, "High", Severity=5, "Critical")
| convert ctime(FirstDetect) ctime(FirstAssign) ctime(ResolvedTime)
| fillnull value="-" FirstAssign, ResolvedTime, MinutesToAssign, HoursFromAssignToClose, DaysFromDetectToClose 
| table ComputerName, Severity, Tactics, Techniques, FirstDetect, FirstAssign, MinutesToAssign, ResolvedTime, HoursFromAssignToClose, DaysFromDetectToClose, detection_id 
| sort + FirstDetect
```

## Query 7
```cql
[...]
| stats avg(DaysFromDetectToClose) as DaysFromDetectToClose by Severity
| eval DaysFromDetectToClose=round(DaysFromDetectToClose,2)
```

## Query 8
```cql
[...]
| stats avg(DaysFromDetectToClose) as DaysFromDetectToClose, avg(HoursFromAssignToClose) as HoursFromAssignToClose, avg(MinutesToAssign) as MinutesToAssign by Severity
| eval DaysFromDetectToClose=round(DaysFromDetectToClose,2)
| eval HoursFromAssignToClose=round(HoursFromAssignToClose,2)
| eval MinutesToAssign=round(MinutesToAssign,2)
```
