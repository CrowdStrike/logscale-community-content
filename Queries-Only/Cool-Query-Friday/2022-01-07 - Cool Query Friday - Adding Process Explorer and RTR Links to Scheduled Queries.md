---
title: "Adding Process Explorer and RTR Links to Scheduled Queries"
date: 2022-01-07
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/ry6ma0/20220107_cool_query_friday_adding_process/"
mitre: []
series: Cool Query Friday
---

# Adding Process Explorer and RTR Links to Scheduled Queries

> Source: [https://www.reddit.com/r/crowdstrike/comments/ry6ma0/20220107_cool_query_friday_adding_process/](https://www.reddit.com/r/crowdstrike/comments/ry6ma0/20220107_cool_query_friday_adding_process/) — by Andrew-CS (CrowdStrike) — 2022-01-07

Welcome to our thirty-fourth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
[...]
| eval CommandLine=lower(CommandLine)
| regex CommandLine=".*group\s+.*admin.*"
```

## Query 2
```cql
[...]
| stats count(aid) as executionCount, latest(TargetProcessId_decimal) as latestFalconPID by aid, ComputerName, UserName, UserSid_readable, FileName, CommandLine
```

## Query 3
```cql
index=main sourcetype=ProcessRollup* event_platform=win event_simpleName=ProcessRollup2 FileName IN (net.exe, net1.exe)
| eval CommandLine=lower(CommandLine)
| regex CommandLine=".*group\s+.*admin.*"
| stats count(aid) as executionCount, latest(TargetProcessId_decimal) as latestFalconPID by aid, ComputerName, UserName, UserSid_readable, FileName, CommandLine
| sort + executionCount
```

## Query 4
```cql
[...]
| eval processExplorer="https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . latestFalconPID
```

## Query 5
```cql
[...]
| eval startRTR="https://falcon.crowdstrike.com/activity/real-time-response/console/?start=hosts&aid=".aid
```

## Query 6
```cql
index=main sourcetype=ProcessRollup* event_platform=win event_simpleName=ProcessRollup2 FileName IN (net.exe, net1.exe)
| fields aid, TargetProcessId_decimal, ComputerName, UserName, UserSid_readable, FileName, CommandLine
| eval CommandLine=lower(CommandLine)
| regex CommandLine=".*group\s+.*admin.*"
| stats count(aid) as executionCount, latest(TargetProcessId_decimal) as latestFalconPID by aid, ComputerName, UserName, UserSid_readable, FileName, CommandLine
| sort + executionCount
| eval processExplorer="https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . latestFalconPID
| eval startRTR="https://falcon.crowdstrike.com/activity/real-time-response/console/?start=hosts&aid=".aid
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
// Specify data source and simpleName (index)
#type = FDR "#event_simpleName" = ProcessRollup2

// search for net.exe and net1.exe (including path, hence the wildcard)
| ImageFileName =~ in(values=["*\\net.exe", "*\\net1.exe"])

// search commandline (case insenitive) 
| CommandLine =~ regex(".*group\s+.*admin.*", flags="i")

// group data and summarize
| groupBy(["#cid", "aid", "UserSid", "ImageFileName", "CommandLine"], function=[count(as=executionCount), selectLast(["TargetProcessId"])])

// enrich sid -> username and aid -> ComputerName, not in the ProcessRollup event when through FDR
| join({#type = FDR #event_simpleName = "UserIdentity" | groupBy(["#cid", "aid", "UserSid"], function=selectLast(["UserName"]))}, include="UserName", field=["#cid", "aid", "UserSid"])
| join({#type = FDR #event_simpleName!=* EventType != "Event_ExternalApiEvent" | groupBy(["#cid", "aid"], function=selectLast(["ComputerName"]))}, include="ComputerName", field=["#cid", "aid"])

// Create RTR and PE links, Humio supports markdown!
| RTR := format("[RTR](https://falcon.eu-1.crowdstrike.com/activity/real-time-response/console/?start=hosts&aid=%s)",field=["aid"])
| "Process Explorer" := format("[Explore](https://falcon.eu-1.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "TargetProcessId"])

// Split string to only get filename
| FileName := splitString(field="ImageFileName", by="\\\\", index="-1")

// Table the output!
| table(["aid", "ComputerName", "UserName", "FileName", "UserSid", "CommandLine", "executionCount", "TargetProcessId", "RTR", "Process Explorer"])
```
— [Community] ts-kra · comment score 3

```cql
"Process Explorer.region" := ?region
| "Process Explorer.region" := upper("Process Explorer.region")
| case {
    "Process Explorer.region" =  "US-1" | "Process Explorer" := format("[Process Explorer](https://falcon.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "TargetProcessId"]);
    "Process Explorer.region" = "US-2" | "Process Explorer" := format("[Process Explorer](https://falcon.us-2.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "TargetProcessId"]);
    "Process Explorer.region" = "EU" | "Process Explorer" := format("[Process Explorer](https://falcon.eu-1.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "TargetProcessId"]);
    "Process Explorer.region" = "GOV" | "Process Explorer" := format("[Process Explorer](https://falcon.laggar.gcw.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "TargetProcessId"]);
    @function.error := "Invalid region selected!"
}
```
— [Community] ts-kra · comment score 3

```cql
[...]
| eval CommandLine=lower(CommandLine)
| regex CommandLine=".*group\s+.*admin.*" 
[...]
```
— [CS] Andrew-CS · comment score 3
