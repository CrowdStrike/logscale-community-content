---
title: "Creating Your Own, Bespoke Hunting Repo with Falcon LTR"
date: 2023-08-04
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/15i3i80/20230804_cool_query_friday_creating_your_own/"
mitre: [T1562.001]
series: Cool Query Friday
---

# Creating Your Own, Bespoke Hunting Repo with Falcon LTR

> Source: [https://www.reddit.com/r/crowdstrike/comments/15i3i80/20230804_cool_query_friday_creating_your_own/](https://www.reddit.com/r/crowdstrike/comments/15i3i80/20230804_cool_query_friday_creating_your_own/) — by Andrew-CS (CrowdStrike) — 2023-08-04

Welcome to our sixtieth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/) (sexagenarian!). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
#event_simpleName=CommandHistory event_platform=Win CommandHistory=/(csagent|csfalcon)/i
```

## Query 2
```cql
#event_simpleName=CommandHistory event_platform=Win CommandHistory=/(csagent|csfalcon)/i
| groupBy([ApplicationName, UserName, UserSid])
```

## Query 3
```cql
#event_simpleName=CommandHistory event_platform=Win CommandHistory=/(csagent|csfalcon)/i ApplicationName!="cmd.exe"
```

## Query 4
```cql
#event_simpleName=CommandHistory event_platform=Win CommandHistory=/(csagent|csfalcon)/i
| HuntingLeadID:=1
```

## Query 5
```cql
#event_simpleName=CommandHistory event_platform=Win CommandHistory=/(csagent|csfalcon)/i
| HuntingLeadID:=1
| HuntingLeadName:="UnexpectedFalconProcessCall"
| ATT&CK:="T1562.001"
| Description:="The CrowdStrike Falcon driver or process name was unexpected invoked from the command line."
```

## Query 6
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\whoami\.exe/i
| groupBy([ParentBaseFileName])
| sort(_count, order=desc)
```

## Query 7
```cql
​​#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\whoami\.exe/i ParentBaseFileName="cmd.exe"
| groupBy([UserSid])
| sort(_count, order=desc)
```

## Query 8
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\whoami\.exe/i
| HuntingLeadID:=2
```

## Query 9
```cql
HuntingLeadID=*
| HuntingLeadID =~ match(file="HuntingLeadID.csv", column=HuntingLeadID, strict=false)
| LeadName=*
| groupBy([aid, ComputerName], function=([sum(Weight, as=Weight), count(HuntingLeadID, as=totalLeads), collect([LeadName]), min(@timestamp, as=firstLead), max(@timestamp, as=lastLead)]))
| firstLead:=formatTime(format="%F %T.%L", field="firstLead")
| lastLead:=formatTime(format="%F %T.%L", field="lastLead")
| sort(Weight, order=desc)
```

## Query 10
```cql
HuntingLeadID=*
| HuntingLeadID =~ match(file="HuntingLeadID.csv", column=HuntingLeadID, strict=false)
| sankey(source="ComputerName", target="LeadName", weight=sum(Weight))
```
