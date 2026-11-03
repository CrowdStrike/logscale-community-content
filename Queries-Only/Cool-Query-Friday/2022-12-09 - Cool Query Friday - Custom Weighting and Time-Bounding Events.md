---
title: "Custom Weighting and Time-Bounding Events"
date: 2022-12-09
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/zh7k5a/20221209_cool_query_friday_custom_weighting_and/"
mitre: []
series: Cool Query Friday
---

# Custom Weighting and Time-Bounding Events

> Source: [https://www.reddit.com/r/crowdstrike/comments/zh7k5a/20221209_cool_query_friday_custom_weighting_and/](https://www.reddit.com/r/crowdstrike/comments/zh7k5a/20221209_cool_query_friday_custom_weighting_and/) — by Andrew-CS (CrowdStrike) — 2022-12-09

Welcome to our fifty-third installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Get all Windows ProcessRollup2 Events
#event_simpleName=ProcessRollup2 event_platform=Win
// Narrow to processes of interest and create FileName variable
| ImageFileName=/\\(?<FileName>(whoami|net1?|systeminfo|ping|nltest|sc|hostname|ipconfig)\.exe)/i
```

## Query 2
```cql
// Get timestamp value with date and hour value
| ProcessStartTime := ProcessStartTime*1000
| dayBucket := formatTime("%Y-%m-%d %H", field=ProcessStartTime, locale=en_US, timezone=Z)
// Force CommandLine and FileName into lower case
| CommandLine := lower(CommandLine)
| FileName := lower(FileName)
```

## Query 3
```cql
// Parse flag used in "net" and "sc" command
| regex("(sc|net1?)\s+(?<netFlag>\S+)\s+", field=CommandLine, strict=false)
// Force netFlag to lower case
| netFlag := lower(netFlag)
```

## Query 4
```cql
/ Create evaluation criteria and weighting for process usage; modified behaviorWeight integer as desired
| case {
        FileName=/net1?\.exe/ AND netFlag="start" | behaviorWeight := "4" ;
        FileName=/net1?\.exe/ AND netFlag="stop" | behaviorWeight := "4" ;
        FileName=/net1?\.exe/ AND netFlag="stop" AND CommandLine=/falcon/i | behaviorWeight := "25" ;
        FileName=/sc\.exe/ AND netFlag="start" | behaviorWeight := "4" ;
        FileName=/sc\.exe/ AND netFlag="stop" | behaviorWeight := "4" ;
        FileName=/sc\.exe/ AND netFlag=/(query|stop)/i AND CommandLine=/csagent/i | behaviorWeight := "25" ;
        FileName=/net1?\.exe/ AND netFlag="share" | behaviorWeight := "2" ;
        FileName=/net1?\.exe/ AND netFlag="user" AND CommandLine=/\/delete/i | behaviorWeight := "10" ;
        FileName=/net1?\.exe/ AND netFlag="user" AND CommandLine=/\/add/i | behaviorWeight := "10" ;
        FileName=/net1?\.exe/ AND netFlag="group" AND CommandLine=/\/domain\s+/i | behaviorWeight := "5" ;
        FileName=/net1?\.exe/ AND netFlag="group" AND CommandLine=/admin/i | behaviorWeight := "5" ;
        FileName=/net1?\.exe/ AND netFlag="localgroup" AND CommandLine=/\/add/i | behaviorWeight := "10" ;
        FileName=/net1?\.exe/ AND netFlag="localgroup" AND CommandLine=/\/delete/i | behaviorWeight := "10" ;
        FileName=/nltest\.exe/ | behaviorWeight := "3" ;
        FileName=/systeminfo\.exe/ | behaviorWeight := "3" ;
        FileName=/whoami\.exe/ | behaviorWeight := "3" ;
        FileName=/ping\.exe/ | behaviorWeight := "3" ;
        FileName=/ipconfig\.exe/ | behaviorWeight := "3" ;
        FileName=/hostname\.exe/ | behaviorWeight := "3" ;
  * }
| default(field=behaviorWeight, value=0)
```

## Query 5
```cql
// Create FileName and CommandLine one-liner
| format(format="(Score: %s) %s • %s", field=[behaviorWeight, FileName, CommandLine], as="executionDetails")
// Group and organize output
| groupby([cid,aid, dayBucket], function=[count(FileName, distinct=true, as="fileCount"), sum(behaviorWeight, as="behaviorWeight"), collect(executionDetails)], limit=max)
```

## Query 6
```cql
| dayBucket := formatTime("%Y-%m-%d, field=ProcessStartTime, locale=en_US, timezone=Z)
```

## Query 7
```cql
// Set thresholds 
| fileCount >= 5 OR behaviorWeight > 30
// Add Host Search link
| format("[Host Search](https://falcon.crowdstrike.com/investigate/events/en-us/app/eam2/investigate__computer?earliest=-24h&latest=now&computer=*&aid_tok=%s&customer_tok=*)", field=["aid"], as="Host Search")
// Sort descending by behavior weighting 
| sort(behaviorWeight)
```

## Query 8
```cql
// Get all Windows ProcessRollup2 Events
#event_simpleName=ProcessRollup2 event_platform=Win
// Narrow to processes of interest and create FileName variable
| ImageFileName=/\\(?<FileName>(whoami|net1?|systeminfo|ping|nltest|sc|hostname|ipconfig)\.exe)/i
// Get timestamp value with date and hour value
| ProcessStartTime := ProcessStartTime*1000
| dayBucket := formatTime("%Y-%m-%d %H", field=ProcessStartTime, locale=en_US, timezone=Z)
// Force CommandLine and FileName into lower case
| CommandLine := lower(CommandLine)
| FileName := lower(FileName)
// Parse flag used in "net" command
| regex("(sc|net1?)\s+(?<netFlag>\S+)\s+", field=CommandLine, strict=false)
// Force netFlag to lower case
| netFlag := lower(netFlag)
// Create evaulation criteria and weighting for process usage; modified behaviorWeight integer as desired
| case {
       FileName=/net1?\.exe/ AND netFlag="start" | behaviorWeight := "4" ;
       FileName=/net1?\.exe/ AND netFlag="stop" | behaviorWeight := "4" ;
       FileName=/net1?\.exe/ AND netFlag="stop" AND CommandLine=/falcon/i | behaviorWeight := "25" ;
       FileName=/sc\.exe/ AND netFlag="start" | behaviorWeight := "4" ;
       FileName=/sc\.exe/ AND netFlag="stop" | behaviorWeight := "4" ;
       FileName=/sc\.exe/ AND netFlag=/(query|stop)/i AND CommandLine=/csagent/i | behaviorWeight := "25" ;
       FileName=/net1?\.exe/ AND netFlag="share" | behaviorWeight := "2" ;
       FileName=/net1?\.exe/ AND netFlag="user" AND CommandLine=/\/delete/i | behaviorWeight := "10" ;
       FileName=/net1?\.exe/ AND netFlag="user" AND CommandLine=/\/add/i | behaviorWeight := "10" ;
       FileName=/net1?\.exe/ AND netFlag="group" AND CommandLine=/\/domain\s+/i | behaviorWeight := "5" ;
       FileName=/net1?\.exe/ AND netFlag="group" AND CommandLine=/admin/i | behaviorWeight := "5" ;
       FileName=/net1?\.exe/ AND netFlag="localgroup" AND CommandLine=/\/add/i | behaviorWeight := "10" ;
       FileName=/net1?\.exe/ AND netFlag="localgroup" AND CommandLine=/\/delete/i | behaviorWeight := "10" ;
       FileName=/nltest\.exe/ | behaviorWeight := "3" ;
       FileName=/systeminfo\.exe/ | behaviorWeight := "3" ;
       FileName=/whoami\.exe/ | behaviorWeight := "3" ;
       FileName=/ping\.exe/ | behaviorWeight := "3" ;
       FileName=/hostname\.exe/ | behaviorWeight := "3" ;
       FileName=/ipconfig\.exe/ | behaviorWeight := "3" ;
 * }
| default(field=behaviorWeight, value=0)
// Create FileName and CommandLine one-liner
| format(format="(Score: %s) %s • %s", field=[behaviorWeight, FileName, CommandLine], as="executionDetails")
// Group and organize output
| groupby([cid,aid, dayBucket], function=[count(FileName, distinct=true, as="fileCount"), sum(behaviorWeight, as="behaviorWeight"), collect(executionDetails)], limit=max)
// Set thresholds
| fileCount >= 5 OR behaviorWeight > 30
// Add Host Search link
| format("[Host Search](https://falcon.crowdstrike.com/investigate/events/en-us/app/eam2/investigate__computer?earliest=-24h&latest=now&computer=*&aid_tok=%s&customer_tok=*)", field=["aid"], as="Host Search")
// Sort descending by behavior weighting
| sort(behaviorWeight)
```

## Query 9
```cql
event_platform=win event_simpleName=ProcessRollup2 FileName IN (net.exe, net1.exe, whoami.exe, ping.exe, nltest.exe,sc.exe, hostname.exe)
| rex field=CommandLine "(sc|net)\s+(?<netFlag>\S+)\s+.*"
| eval netFlag=lower(netFlag), CommandLine=lower(CommandLine), FileName=lower(FileName)
| eval behaviorWeight=case(
  (FileName == "net.exe" OR FileName == "net1.exe") AND netFlag=="start",  "2",
  (FileName == "net.exe" OR FileName == "net1.exe") AND netFlag=="stop",  "4",
  (FileName == "net.exe" OR FileName == "net1.exe") AND netFlag=="share",  "4",
  (FileName == "net.exe" OR FileName == "net1.exe") AND (netFlag=="user"  AND CommandLine LIKE "%delete%"),  "10",
  (FileName == "net.exe" OR FileName == "net1.exe") AND (netFlag=="user"  AND CommandLine LIKE "%add%"),  "10",
  (FileName == "net.exe" OR FileName == "net1.exe") AND (netFlag=="group" AND CommandLine LIKE "%domain%"),  "5",
  (FileName == "net.exe" OR FileName == "net1.exe") AND (netFlag=="group" AND CommandLine LIKE "%admin%"),  "5",
  (FileName == "net.exe" OR FileName == "net1.exe") AND (netFlag=="localgroup" AND CommandLine LIKE "%add%"),  "10",
  (FileName == "net.exe" OR FileName == "net1.exe") AND (netFlag=="localgroup" AND CommandLine LIKE "%delete%"),  "10",
  (FileName == "sc.exe") AND (netFlag=="stop" AND CommandLine LIKE "%csagent%"),  "4",
  FileName == "whoami.exe",  "3",
  FileName == "ping.exe",  "3",
  FileName == "nltest.exe",  "3",
  FileName == "systeminfo.exe",  "3",
  FileName == "hostname.exe",  "3",
  true(),null()) 
  | bucket ProcessStartTime_decimal as timeBucket span=1h
  | stats dc(FileName) as fileCount, sum(behaviorWeight) as behaviorWeight, values(FileName) as filesSeen, values(CommandLine) as commandLines by timeBucket, aid, ComputerName
  | where fileCount >= 5 
  | eval hostSearch=case(aid!="","https://falcon.crowdstrike.com/investigate/events/en-us/app/eam2/investigate__computer?earliest=".timeBucket."&latest=now&computer=*&aid_tok=".aid)
  | sort -behaviorWeight, -fileCount
  | convert ctime(timeBucket)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> >What is the purpose of true(),null() in the case statement? This basically says, "if you do not match any of the case statements, set that value of the field `behaviorWeight` to null" (so it will be blank). >In the Event Search version, should 'OR behaviorWeight > 30' be added to the fourth line from the end '| where fileCount > 5'? Yup! You can add conditions for matching if you'd like!
— [CS] Andrew-CS · score 2

### Q&A

**Q — [Community] Qbert513:** Two questions: 1. What is the purpose of true(),null() in the case statement? 2. In the Event Search version, should 'OR behaviorWeight > 30' be added to the fourth line from the end '| where fileCount > 5'?

**A — [CS] Andrew-CS:** >What is the purpose of true(),null() in the case statement? This basically says, "if you do not match any of the case statements, set that value of the field `behaviorWeight` to null" (so it will be blank). >In the Event Search version, should 'OR behaviorWeight > 30' be added to the fourth line from the end '| where fileCount > 5'? Yup! You can add conditions for matching if you'd like!
